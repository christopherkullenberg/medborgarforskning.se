#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the ARCServer container and mount the volumes for the nginx server
FROM nginx
#COPY ./share/nginx/html/ /share/nginx/html/
COPY arcsApp /share/nginx/static/
COPY arcsApp /share/nginx/media/
COPY ./nginx.conf .
#VOLUME /usr/share/nginx/html/
VOLUME /usr/share/nginx/static/
VOLUME /usr/share/nginx/media/
VOLUME /etc/nginx/



# Builds the ARCSapp container mounting the volumes for the django app and run the configuration
FROM python:3.7

# recommended by django https://docs.docker.com/compose/django/
ENV PYTHONUNBUFFERED 1

#update packages
RUN apt-get clean && apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv

# create virtual environment for total python control #TODO install python packages in virutalenv
# RUN python -m virtualenv --python=/usr/bin/python3 /opt/venv
# RUN python -m venv --python=/usr/bin/python3 /opt/venv

# update pip
#RUN pip install --upgrade pip
#RUN . /opt/venv/bin/activate && pip install --upgrade pip

# install our two dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# arbitrary location choice: you can change the directory
RUN mkdir -p /var/www/arcsApp/
WORKDIR /var/www/arcsApp/

# copy project code
COPY arcsApp /var/www/arcsApp/

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
# CMD ["gunicorn", "--chdir", "hello", "--bind", ":8000", "hello.wsgi:application"]
# RUN python manage.py runserver 0.0.0.0:8000
# RUN . /opt/venv/bin/activate && exec python ./manage.py runserver 0.0.0.0:8000
#RUN uwsgi --http :8000 --wsgi-file test.py