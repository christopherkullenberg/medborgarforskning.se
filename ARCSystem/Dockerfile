#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the ARCSapp container mounting the volumes for the django app and run the configuration
FROM python:3.7

# recommended by django https://docs.docker.com/compose/django/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#update packages
RUN apt-get clean && apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv uwsgi-emperor libssl-dev

# create virtual environment for total python control #TODO install python packages in virutalenv
# RUN python -m virtualenv --python=/usr/bin/python3 /opt/venv

# update pip
RUN pip install --upgrade pip
#RUN . /opt/venv/bin/activate && pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# arbitrary location choice: you can change the directory
# RUN mkdir -p /var/www/arcsApp/
# WORKDIR /var/www/arcsApp/
RUN mkdir -p /arcsApp/
WORKDIR /arcsApp/

# copy project code to container
#COPY arcsApp /var/www/arcsApp/
COPY ./arcsApp/ .

# expose the port 8000
 EXPOSE 8000

# start the wsgi server and load configuration file uwsgi.ini
#RUN uwsgi --ini uwsgi.ini
# RUN uwsgi --http :8000 --wsgi-file test.py --uid 100 --gid 100 --daemonize=/var/log/uwsgi/yourproject.log
# RUN uwsgi --socket :8000 --wsgi-file test.py --uid 100 --gid 100 --master
# RUN python manage.py runserver 0.0.0.0:8000

#CMD python test.py
# define the default command to run when starting the container
# CMD ["gunicorn", "--chdir", "hello", "--bind", ":8000", "hello.wsgi:application"]
#RUN python manage.py runserver 0.0.0.0:8000
# RUN . /opt/venv/bin/activate && exec python ./manage.py runserver 0.0.0.0:8000
#RUN uwsgi --http :8000 --wsgi-file test.py
