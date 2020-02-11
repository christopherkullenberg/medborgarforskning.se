#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the Arcs_app container mounting the volumes for the django app and run the configuration
FROM python:3.7

LABEL maintainer="TBA"
LABEL vendor="TBA"

# recommended by django https://docs.docker.com/compose/django/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#update packages
RUN apt-get clean && apt-get update && apt-get install \
  -y --no-install-recommends python3 uwsgi-emperor \
  libssl-dev pipenv

# arbitrary location choice: you can change the directory
RUN mkdir -p /arcs_project_code/
WORKDIR /arcs_project_code

# create virtual environment for total python control #TODO install python \
COPY Pipfile Pipfile.lock /arcs_project_code/
RUN pip install pipenv && pipenv install --system

# update pip
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt



# copy project code to container
COPY . .

# expose the port 8000
 EXPOSE 8000
