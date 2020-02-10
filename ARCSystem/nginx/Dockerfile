#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the ARCServer container and mount the volumes for the nginx server
FROM nginx
#update packages
RUN apt-get clean && apt-get update && apt-get install \
  -y --no-install-recommends

COPY arcsApp /share/nginx/static/
COPY arcsApp /share/nginx/media/
COPY nginx.conf .
VOLUME /usr/share/nginx/static/
VOLUME /usr/share/nginx/media/
VOLUMEOLUME /etc/nginx/
