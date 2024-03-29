FROM python:3.8-slim
MAINTAINER Tyler Fowler <tylerfowler.1337@gmail.com>

# Superset setup options
ENV SUPERSET_VERSION 0.37.2
ENV SUPERSET_HOME /superset
ENV SUP_ROW_LIMIT 5000
ENV SUP_WEBSERVER_THREADS 8
ENV SUP_WEBSERVER_WORKERS 10
ENV SUP_WEBSERVER_PORT 8088
ENV SUP_WEBSERVER_TIMEOUT 60
ENV SUP_SECRET_KEY 'thisismysecretkey'
ENV SUP_META_DB_URI "sqlite:///${SUPERSET_HOME}/superset.db"
ENV SUP_CSRF_ENABLED True
ENV SUP_CSRF_EXEMPT_LIST []
ENV MAPBOX_API_KEY ''

ENV PYTHONPATH $SUPERSET_HOME:$PYTHONPATH

# admin auth details
ENV ADMIN_USERNAME admin
ENV ADMIN_FIRST_NAME admin
ENV ADMIN_LAST_NAME user
ENV ADMIN_EMAIL admin@nowhere.com
ENV ADMIN_PWD superset

# by default only includes PostgreSQL because I'm selfish
ENV DB_PACKAGES libpq-dev
ENV DB_PIP_PACKAGES psycopg2-binary sqlalchemy-redshift

RUN apt-get update \
&& apt-get install -y \
  $DB_PACKAGES \
  build-essential gcc git \
  libssl-dev libffi-dev libsasl2-dev libldap2-dev \
&& pip install --no-cache-dir \
  $DB_PIP_PACKAGES apache-superset==$SUPERSET_VERSION \
  email_validator gunicorn[gevent] \
&& apt-get remove -y \
  build-essential libssl-dev libffi-dev libsasl2-dev libldap2-dev git \
&& apt-get -y autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
&& apt-get autoremove -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# remove build dependencies
RUN mkdir $SUPERSET_HOME

COPY superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

VOLUME $SUPERSET_HOME
EXPOSE 8088

# since this can be used as a base image adding the file /docker-entrypoint.sh
# is all you need to do and it will be run *before* Superset is set up
ENTRYPOINT [ "/superset-init.sh" ]
