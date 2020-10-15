FROM nvcr.io/nvidia/pytorch:20.08-py3

# Force stdin, stdout and stderr to be totally unbuffered. Good for logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends nginx curl

WORKDIR /opt/ml/

RUN pip install fastai==2.0.0
RUN pip install fastcore==1.0.0
RUN pip install ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension

COPY src/ /opt/ml/code

ENV PATH="/opt/ml/code:${PATH}"