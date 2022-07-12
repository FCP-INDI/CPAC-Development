# Copyright (C) 2022  C-PAC Developers
# 
# This file is part of CPAC-Development.
# 
# CPAC-Development is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# 
# CPAC-Development is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License along with CPAC-Development. If not, see <https://www.gnu.org/licenses/>.
ARG DEPRECATED_VERSION
FROM fcpindi/c-pac:${DEPRECATED_VERSION}-DEPRECATED
ARG DEPRECATED_VERSION
COPY ./CRITICAL_ALERT.rst /CRITICAL_ALERT.rst
COPY ./bash.bashrc /etc/bash.bashrc
RUN sed -i "s|\${DEPRECATED_VERSION}|${DEPRECATED_VERSION}|g" /CRITICAL_ALERT.rst && \
  sed -i "s|\${RECOMMENDED_MINIMUM_VERSION}|${RECOMMENDED_MINIMUM_VERSION}|g" /CRITICAL_ALERT.rst
COPY ./cpac_pipeline.py /code/CPAC/pipeline/cpac_pipeline.py
COPY ./run.py /code/run.py
