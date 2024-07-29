FROM python:3.11.8


RUN apt-get -y update && \
    pip install --upgrade pip && \
    apt-get install --no-install-recommends -y \
    build-essential && \
    pip install --upgrade poetry && \
    apt install -y chromium


WORKDIR /stripe-price

COPY . .

RUN poetry install
