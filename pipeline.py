from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf
from pyflink.datastream import StreamExecutionEnvironment

import tokenizer
import pandas as pd
from gensim.models.ldamodel import LdaModel
from gensim.corpora import Dictionary


ddl_jdbc_source = """CREATE TABLE user_ml_messages (
                            message_date TIMESTAMP(3),
                            message_id STRING,
                            message_in_reply_to STRING,
                            message_from_name STRING,
                            message_from_email STRING,
                            message_subject STRING,
                            proc_time AS PROCTIME(),
                            PRIMARY KEY(message_id) NOT ENFORCED
                    ) WITH (
                        'connector'= 'jdbc',
                        'url' = 'jdbc:postgresql://postgres:5432/postgres',
                        'table-name' = 'perceval.stg_flink_user_ml',
                        'username' = 'postgres',
                        'password' = 'postgres'
                    )"""

ddl_jdbc_dim = """CREATE TABLE dim_topics (
                        id VARCHAR(2),
                        topic VARCHAR(50),
                        topic_weigh VARCHAR(100),
                        PRIMARY KEY(id) NOT ENFORCED
                  ) WITH (
                      'connector'= 'jdbc',
                      'url' = 'jdbc:postgresql://postgres:5432/postgres',
                      'table-name' = 'perceval.dim_topics',
                      'username' = 'postgres',
                      'password' = 'postgres'
                )"""

ddl_jdbc_sink = """CREATE TABLE flink_user_ml_topics (
                        message_id STRING,
                        message_date TIMESTAMP(3),
                        message_from_name STRING,
                        topic VARCHAR(2),
                        topic_description VARCHAR(50),
                        PRIMARY KEY(message_id) NOT ENFORCED
                ) WITH (
                    'connector'= 'jdbc',
                    'url' = 'jdbc:postgresql://postgres:5432/postgres',
                    'table-name' = 'perceval.flink_user_ml_topics',
                    'username' = 'postgres',
                    'password' = 'postgres'
                )"""


@udf(input_types=DataTypes.STRING(), result_type=DataTypes.STRING(), udf_type='pandas')
def class_model(m):

    lda = LdaModel.load("model/lda_model/lda_model_user_ml")

    dic = Dictionary.load('model/lda_model/lda_model_user_ml.id2word')

    topics = [tokenizer.find_topic(message, lda, dic) for message in m]

    return pd.Series(topics)


if __name__ == '__main__':

  env = StreamExecutionEnvironment.get_execution_environment()
  env.set_parallelism(1)
  t_env = StreamTableEnvironment.create(env)

  t_env.add_python_file("/opt/pyflink-nlp/tokenizer.py")
  t_env.add_python_archive(archive_path="/opt/pyflink-nlp/lda_model.zip#model", target_dir=None)

  config = t_env.get_config().get_configuration()
  config.set_string("taskmanager.memory.task.off-heap.size", "80mb") #512mb

  create_jdbc_source = t_env.execute_sql(ddl_jdbc_source)
  create_jdbc_sink = t_env.execute_sql(ddl_jdbc_sink)
  create_jdbc_dim = t_env.execute_sql(ddl_jdbc_dim)

  # Register the UDF in the Table Environment
  t_env.register_function("CLASS_TOPIC", class_model)

  # 
  t_env.execute_sql("""INSERT INTO flink_user_ml_topics
                                  WITH topics AS (SELECT message_id,
                                                         message_date,
                                                         message_from_name,
                                                         CLASS_TOPIC(message_subject) AS topic_id,
                                                         proc_time
                                                  FROM user_ml_messages
                                                  WHERE message_subject IS NOT NULL
                                                  )
                                  SELECT t.message_id,
                                         t.message_date,
                                         t.message_from_name,
                                         t.topic_id,
                                         dim.topic AS topic_name
                                  FROM topics t
                                  JOIN dim_topics FOR SYSTEM_TIME AS OF t.proc_time AS dim
                                   ON t.topic_id = dim.id
                              """)