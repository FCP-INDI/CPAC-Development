ARG DEPRECATED_VERSION
FROM fcpindi/c-pac:${DEPRECATED_VERSION}-DEPRECATED
ARG DEPRECATED_VERSION
COPY ./CRITICAL_ALERT.rst /CRITICAL_ALERT.rst
COPY ./bash.bashrc /etc/bash.bashrc
RUN sed -i "s|\${DEPRECATED_VERSION}|${DEPRECATED_VERSION}|g" /CRITICAL_ALERT.rst
COPY ./cpac_pipeline.py /code/CPAC/pipeline/cpac_pipeline.py
COPY ./run.py /code/run.py
