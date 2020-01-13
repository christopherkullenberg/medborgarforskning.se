#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# mount the volumes for the nginx server
FROM nginx
#COPY ./share/nginx/html/ /share/nginx/html/
COPY ./arcsApp/static/ /share/nginx/static/
COPY ./arcsApp/media/ /share/nginx/media/
COPY ./nginx.conf .
#VOLUME /usr/share/nginx/html/
VOLUME /usr/share/nginx/static/
VOLUME /usr/share/nginx/media/
VOLUME /etc/nginx/

# mount the volumes for the django app and run the configuration
FROM python:3.6

# arbitrary location choice: you can change the directory
RUN mkdir -p /var/www/arcsApp/
WORKDIR /var/www/arcsApp/


# install our two dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy our project code
COPY ./arcsApp/ /var/www/arcsApp/


# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
# CMD ["gunicorn", "--chdir", "hello", "--bind", ":8000", "hello.wsgi:application"]
RUN python3 ./manage.py runserver 0.0.0.0:8000
