#
# File Name: Dockerfile
# Description: Setup the nginx docker container.
# Author: Jonathan Brier & Christopher Kullenberg
#

# Builds the ARCServer container and mount the volumes for the nginx server
FROM nginx

#COPY arcs_project /share/nginx/static/
#COPY arcs_project /share/nginx/media/
COPY nginx.conf /etc/nginx/
#VOLUME /usr/share/nginx/static/
#VOLUME /usr/share/nginx/media/
#VOLUME /etc/nginx/
