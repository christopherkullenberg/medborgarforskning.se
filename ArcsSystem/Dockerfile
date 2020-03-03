#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the Arcs_app container mounting the volumes for the django app and run the configuration
FROM python:3.7

LABEL maintainer="The ARCS Software Team"
LABEL vendor="None"

# recommended by django https://docs.docker.com/compose/django/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  libssl-dev # TODO check if this is still needed for https

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/arcs_project_code/
WORKDIR /opt/arcs_project_code

COPY entrypoint.sh .

# install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /opt/arcs_project_code/
RUN pipenv install --system

# make directory for collected static files shared with nginx
RUN mkdir -p /var/www/arcs_collected_static/static/

# copy project code to container
COPY . /opt/arcs_project_code/

# start the app
CMD ["entrypoint.sh"] # TODO identify why this does not execute
