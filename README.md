# Building an Analytics Pipeline with PyFlink

> :warning: **Update:** This repository will no longer be actively maintained. Please check the [Ververica fork](https://github.com/ververica/pyflink-nlp).

See the [slides](https://noti.st/morsapaes/2qPOCm/building-an-end-to-end-analytics-pipeline-with-pyflink) for more context.

## Docker

To keep things simple, this demo uses a Docker Compose setup that makes it easier to bundle up all the services you need:

<p align="center">
<img width="750" alt="demo_overview" src="https://user-images.githubusercontent.com/23521087/105339206-b571d100-5bdc-11eb-8fca-925c5c6656f2.png">
</p>

#### Getting the setup up and running
`docker-compose build`

`docker-compose up -d`

#### Is everything really up and running?

`docker-compose ps`

You should be able to access the Flink Web UI (http://localhost:8081), as well as Superset (http://localhost:8088).

## Analyzing the Flink User Mailing List

What are people asking more frequently about in the Flink User Mailing List? How can you make sense of such a huge amount of random text?

### Some Background

The model in this demo was trained using a popular topic modeling algorithm called [LDA](https://towardsdatascience.com/lda-topic-modeling-an-explanation-e184c90aadcd) and [Gensim](https://radimrehurek.com/gensim/), a Python library with a good implementation of the algorithm. The trained model knows to some extent what combination of words are associated with certain topics, and can just be passed as a dependency to PyFlink. 

Don't trust the model. :japanese_ogre:

### Submitting the PyFlink job

```bash
docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink-nlp/pipeline.py \ 
  --pyArchives /opt/pyflink-nlp/lda_model.zip#model \
  --pyFiles /opt/pyflink-nlp/tokenizer.py -d
```

Once you get the `Job has been submitted with JobID <JobId>` green light, you can check and monitor its execution using the [Flink WebUI](http://localhost:8081):

![Flink-Web-UI](https://user-images.githubusercontent.com/23521087/105530322-eab71580-5ce7-11eb-9d21-c2b7d608078e.png)

### Visualizing on Superset

To visualize the results, navigate to (http://localhost:8088) and log into Superset using:

`username: admin`

`password: superset`

There should be a default dashboard named "Flink User Mailing List" listed under `Dashboards`:

![Superset](https://user-images.githubusercontent.com/23521087/105530591-497c8f00-5ce8-11eb-8636-3bad2de7bd90.png)

<hr>

**And that's it!**

For the latest updates on PyFlink, follow [Apache Flink](https://twitter.com/ApacheFlink) on Twitter.