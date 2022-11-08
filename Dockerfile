# pull official base image
FROM python:3.10-alpine as build-python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
APPLICATION_PATH=/usr/src/app/ \
PATH=/root/.local/bin:${PATH}

RUN apk update \
&& apk add --virtual .build-deps \
&& apk add --no-cache librdkafka \
curl \
postgresql-dev \
librdkafka-dev \
libffi-dev \
libxml2-dev \
libxslt-dev \
build-base \
&& curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - \
&& cd /usr/local/bin \
&& ln -s /opt/poetry/bin/poetry \
&& poetry config virtualenvs.create false \
&& poetry config virtualenvs.in-project false

# install dependencies
COPY ./pyproject.toml ./poetry.lock* ${APPLICATION_PATH}
# set work directory
WORKDIR ${APPLICATION_PATH}

# Allow installing dev dependencies to run tests
ARG DEV
ENV DEV ${DEV:-true}
RUN /bin/sh -c "if [ $DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


# use alpline image. final image
FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWIRTEBYTECODE=1 \
APPLICATION_PATH=/usr/src/app/ \
DAGSTER_HOME=/opt/dagster/dagster_home/ \
DJANGO_CONFIGURATION=BaseConfiguration \
DJANGO_SETTINGS_MODULE=threatintel.threatintel.settings

ENV PYTHONPATH /app:$PYTHONPATH

RUN mkdir -p $DAGSTER_HOME

WORKDIR ${APPLICATION_PATH}

# RUN addgroup --system worker \
#     && adduser --no-create-home --system --ingroup worker worker

COPY --from=build-python /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

COPY . ${APPLICATION_PATH}

COPY entrypoint.sh /entrypoint.sh
COPY ./dagster.yaml ${DAGSTER_HOME}

ARG PORT
ENV PORT ${PORT:-8000}

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
