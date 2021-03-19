FROM ubuntu:focal

WORKDIR /openedx/discovery

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install --yes \
    git \
    language-pack-en \
    python3-venv \
    python3.8-dev \
    python3.8-venv \
    build-essential \
    libffi-dev \
    libmysqlclient-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libssl-dev \
  && rm -rf /var/lib/apt/lists/*

# Setup system locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Setup python dependencies
ENV VIRTUAL_ENV=/venv
RUN python3.8 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install pip==20.2.3 setuptools==50.3.0 nodeenv

# Add node dependencies
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN nodeenv /edx/app/nodeenv --node=12.11.1 --prebuilt
ENV PATH /edx/app/nodeenv/bin:${PATH}
RUN npm install --production
COPY bower.json bower.json
RUN ./node_modules/.bin/bower install --allow-root --production

# Add the rest of the requirements
ADD . /openedx/discovery

# Install requirements
COPY requirements/ requirements/
RUN make production-requirements \
  && pip install python-json-logger==0.1.11

# Adding placeholders
COPY ./.github/eol.py ./course_discovery/settings/eol.py
COPY ./.github/placeholder.yml /edx/etc/discovery.yml
RUN pip install whitenoise==5.2.0
ENV DJANGO_SETTINGS_MODULE course_discovery.settings.eol


# Compile static files
ENV DISCOVERY_CFG /edx/etc/discovery.yml
RUN make static

EXPOSE 8000
CMD gunicorn --name ecommerce --bind=0.0.0.0:8000 --max-requests=1000 --workers 2 course_discovery.wsgi:application
