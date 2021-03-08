FROM ubuntu:focal as openedx

RUN apt update && DEBIAN_FRONTEND=noninteractive \
  apt install -y git-core \
  tzdata \
  language-pack-en \
  python3-pip \
  python3.8-dev \
  build-essential \
  libffi-dev \
  libmysqlclient-dev \
  libxml2-dev \
  libxslt-dev \
  libjpeg-dev \
  libssl-dev && \
  pip3 install pip==20.2.3 nodeenv setuptools==50.3.0

RUN rm -rf /var/lib/apt/lists/*

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=America/Santiago
RUN locale-gen en_US.UTF-8

COPY . /edx/app/discovery
WORKDIR /edx/app/discovery

ENV DISCOVERY_CFG /edx/etc/discovery.yml

RUN nodeenv /edx/app/nodeenv --node=12.11.1 --prebuilt
ENV PATH /edx/app/nodeenv/bin:${PATH}

# Link for old python scripts
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install -r requirements.txt
RUN npm install --production
RUN ./node_modules/.bin/bower install --allow-root --production

# EOL DIFF
COPY ./.github/eol.py ./course_discovery/settings/eol.py
COPY ./.github/placeholder.yml /edx/etc/discovery.yml
RUN pip install whitenoise==5.2.0
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.eol
RUN make static

EXPOSE 8381
CMD gunicorn --bind=0.0.0.0:8381 --workers 2 --max-requests=1000 -c /edx/app/discovery/course_discovery/docker_gunicorn_configuration.py course_discovery.wsgi:application

FROM openedx as edx.org

RUN pip install newrelic
CMD newrelic-admin run-program gunicorn --bind=0.0.0.0:8381 --workers 2 --max-requests=1000 -c /edx/app/discovery/course_discovery/docker_gunicorn_configuration.py course_discovery.wsgi:application

