FROM ubuntu:16.04

# Install system requirements
RUN apt update && \
    apt install -y --no-install-recommends libpython3.5-minimal python3-dev  python3-pip python3-setuptools nodejs npm nodejs-legacy libmysqlclient-dev mysql-client git make build-essential gcc locales \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && rm /usr/bin/python \
    && ln -s /usr/bin/python3 /usr/bin/python

# Setup system locales, this is used to fix accent in code
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD . /openedx/discovery
WORKDIR /openedx/discovery

RUN make production-requirements \
  && pip3 install python-json-logger==0.1.11 \
  make static

EXPOSE 8000
CMD gunicorn --name ecommerce --bind=0.0.0.0:8000 --max-requests=1000 --workers ${WORKER_COUNT:-1} course_discovery.wsgi:application
