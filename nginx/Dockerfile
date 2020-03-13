#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the ARCServer container and mount the volumes for the nginx server
FROM nginx

### remove the default config files copy the ARCS default nginx.conf
RUN rm /etc/nginx/nginx.conf

### add the ARCS configured nginx.conf to the server image
COPY conf/nginx.conf /etc/nginx/

### add the modular includes for the nginx.conf to the server ###
COPY conf/includes/. /etc/nginx/

### add .well-known static files to server
COPY ./.well-known/ /var/www/.well-known

### copy a custom mime.types file from ARCS to docker image
#RUN rm /etc/nginx/mime.types
#COPY conf/mime.types /etc/nginx/


# shared volume for static files are configured in docker-compose.yaml
