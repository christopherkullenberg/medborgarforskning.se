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
RUN mkdir -p /arcs_project_code/
WORKDIR /arcs_project_code

# install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /arcs_project_code/
RUN pipenv install --system

# copy project code to container
COPY . /arcs_project_code/

# expose the port 8000
 EXPOSE 8000

# start the app
#CMD ["arcs_project/entrypoint.sh"]
