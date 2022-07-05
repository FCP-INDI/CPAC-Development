ARG DEPRECATED_VERSION=release-v1.8.1
FROM fcpindi/c-pac:${DEPRECATED_VERSION}
ARG DEPRECATED_VERSION
COPY ./CRITICAL_ALERT.rst /CRITICAL_ALERT.rst
RUN sed -i "s|\${DEPRECATED_VERSION}|${DEPRECATED_VERSION}|g" /CRITICAL_ALERT.rst
COPY ./cpac_pipeline.py /code/CPAC/pipeline/cpac_pipeline.py
COPY ./run.py /code/run.py
