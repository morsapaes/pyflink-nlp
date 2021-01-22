FROM flink:1.11.2-scala_2.11
ARG FLINK_VERSION=1.11.2

# Install PyFlink
RUN set -ex; \
    apt-get update; \
    apt-get -y install python3; \
    apt-get -y install python3-pip; \
    apt-get -y install python3-dev; \
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/pip3 /usr/bin/pip; \
    apt-get update; \
    python -m pip install --upgrade pip; \
    pip install apache-flink==1.11.2; \
    pip install gensim; \
    pip install spacy; \
    python -m spacy download en;

# Download connector libraries
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc_2.11/${FLINK_VERSION}/flink-connector-jdbc_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/postgresql/postgresql/42.2.12/postgresql-42.2.12.jar;

RUN echo "taskmanager.memory.jvm-metaspace.size: 512m" >> /opt/flink/conf/flink-conf.yaml;
RUN echo "taskmanager.memory.task.off-heap.size: 80mb" >> /opt/flink/conf/flink-conf.yaml;

WORKDIR /opt/flink
