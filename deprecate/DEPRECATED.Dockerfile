ARG DEPRECATED_VERSION
FROM bash
ARG DEPRECATED_VERSION
COPY ./CRITICAL_ALERT.rst /CRITICAL_ALERT.rst
COPY ./entrypoint /entrypoint
RUN sed -i "s|\${DEPRECATED_VERSION}|${DEPRECATED_VERSION}|g" /CRITICAL_ALERT.rst && \
  ln -s /entrypoint /bin/bash
ENTRYPOINT [ "/entrypoint" ]
