FROM ubuntu:18.04

ENV DEBIA_FRONTEND noninteractive

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get update && apt-get install -y --no-install-recommends nginx \
    curl \
    gxx \
    mono-mcs \
    build-essential \
    ca-certificates \
    wget \
    pkg-config 

RUN curl -L -o ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && /opt/conda/bin/conda update conda \
    && /opt/conda/bin/conda install -y \
        python=$PYTHON_VERSION 

RUN pip install jupyterlab 
RUN pip install notebook

COPY config /opt/ml/config

RUN pip install -r /opt/ml/config/requirement.txt

# Add conda to path
ENV PATH=/opt/conda/bin:${PATH}

# Define importants env variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/ml/code:${PATH}"
ENV STAGE=$STAGE

COPY src /opt/ml/code

WORKDIR /opt/ml/code
