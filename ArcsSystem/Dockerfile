#
# File Name: Dockerfile
# Description: Setup the djangoapp docker container.
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
  gettext libssl-dev # TODO check if this is still needed for https

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/arcs_project_code/
WORKDIR /opt/arcs_project_code

COPY entrypoint.sh .

# install dependencies. Note: using pip install instead of pipenv for systemwide container install.
RUN pip install pipenv
RUN pip install wikidata
RUN pip install pillow
RUN pip install psycopg2
RUN pip install django_countries
COPY Pipfile*  /opt/arcs_project_code/

# Note: the requirements.txt must be up to date
RUN cd /opt/arcs_project_code/ && pipenv lock --requirements > requirements.txt
RUN pip install -r /opt/arcs_project_code/requirements.txt

# make directory for collected static files shared with nginx
RUN mkdir -p /var/www/arcs_collected_static/static/

# copy project code to container # TODO consider replacing by volume
COPY . /opt/arcs_project_code/

# remove old static files collected in previous build to ensure only the fresh files are there
RUN rm -r /var/www/arcs_collected_static/static/

# TODO print to console = Bye Bye Old Static Files - Empty! Note: this is a static statement and not a check.

# make sure the translation strings are compiled
RUN python manage.py compilemessages

# collectstatic static on build (but you'll need to run a commands if you're not rebuilding on project code changes)
RUN python manage.py collectstatic --noinput

# start the app # TODO identify why this does not execute
CMD ["entrypoint.sh"]
