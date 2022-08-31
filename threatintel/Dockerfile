# pull official base image
FROM python:3.10-alpine


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache librdkafka librdkafka-dev libxml2-dev libxslt-dev

# install dependencies
RUN apk add build-base
RUN pip install --upgrade pip
COPY ./threatintel/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
#COPY /home/gitlab-runner/.env .env


#EXPOSE 8000

#RUN #python ./threatintel/manage.py collectstatic --noinput
#CMD gunicorn threatintel.wsgi --chdir threatintel --bind 0.0.0.0 --workers=4 -t 0 --preload --log-file -

RUN pip install \
    dagster \
    dagster-graphql \
    dagit \
    dagster-postgres \
    dagster-docker

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR ./threatintel

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME