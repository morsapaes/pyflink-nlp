# Building an Analytics Pipeline with PyFlink

**(WIP)**

See the [slides](https://noti.st/morsapaes/2qPOCm/building-an-end-to-end-analytics-pipeline-with-pyflink) for context.

<p align="center">
<img width="750" alt="demo_overview" src="https://user-images.githubusercontent.com/23521087/105339206-b571d100-5bdc-11eb-8fca-925c5c6656f2.png">
</p>

#### Getting the setup up and running
`docker-compose build`

`docker-compose up -d`

#### Is everything really up and running?

`docker-compose ps`

You should be able to access the Flink Web UI (http://localhost:8081), as well as Superset (http://localhost:8088).

## Submitting the PyFlink job

```bash
docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink-nlp/pipeline.py \ 
  --pyArchives /opt/pyflink-nlp/lda_model.zip#model \
  --pyFiles /opt/pyflink-nlp/tokenizer.py -d
```

Once you get the `Job has been submitted with JobID <JobId>` green light, you can check and monitor its execution using the [Flink WebUI](http://localhost:8081):

![Flink-Web-UI](https://user-images.githubusercontent.com/23521087/105530322-eab71580-5ce7-11eb-9d21-c2b7d608078e.png)

## Superset

To visualize the results, navigate to (http://localhost:8088) and log into Superset using:

`username: admin`

`password: superset`

There should be a default dashboard named "Flink User Mailing List" listed under `Dashboards`:

![Superset](https://user-images.githubusercontent.com/23521087/105530591-497c8f00-5ce8-11eb-8636-3bad2de7bd90.png)

<hr>

**And that's it!**

If you have any questions or feedback, feel free to DM me on Twitter [@morsapaes](https://twitter.com/morsapaes).