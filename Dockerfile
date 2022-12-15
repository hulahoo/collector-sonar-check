
FROM python:3.11-slim as deps
WORKDIR /app
COPY . ./
RUN pip --no-cache-dir install -r requirements.txt 
RUN pip --no-cache-dir install -r requirements.setup.txt 
RUN pip install -e .

FROM deps as build
ARG ARTIFACT_VERSION=local
RUN python setup.py sdist bdist_wheel
RUN ls -ll /app/
RUN ls -ll /app/dist/


FROM python:3.11-slim as runtime
COPY --from=build /app/dist/*.whl /app/
RUN pip --no-cache-dir install /app/*.whl \
    && rm -f /app/*.whl
#USER app
ENTRYPOINT ["events-collector"]
