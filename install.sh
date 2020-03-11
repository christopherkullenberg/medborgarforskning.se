#!/bin/bash
#
# Script Name: install.sh
# Description: basic init script to check for system dependencies and enable
#              controls to manage spinup and configuration
# Author: Jonathan Brier & Christopher Kullenberg
#
#
#
#

###### BEGIN Current manual process from fresh repo ######
# Note: these steps will be extracted to variables to read from ArcsSystem.config and ArcsCore.env
# Note: how the static files is configured the django static files will be collected and placed in a docker volume and recollected on each -build of the django app
# Note: .well-known located in the nginx directory is copied into the nginx folder to server common static files under domain/.well-known/
1. Set domain in init-letsencrypt.sh to get certificate - current default is hard coded for a test url for medborgarforskning.se and arcstest.brierjon.com
2. If you are buliding ARCS Core - set your domains in settings.py Authorized Hosts. - current default is hard coded for a test url for medborgarforskning.se and arcstest.brierjon.com
3. Run sudo docker-compose up --build # on first run this will have nginx on a reboot loop
4. Run the init-letsencrypt.sh with sudo ./init-letsencrypt.sh if you run from the directory it is located - it will generate folders /data /log and /data will be where your certificates are issued
5. Subsquent runs can just sudo docker-compose up or sudo docker-compose up --build depening on your needs.

#Note: on server configuration - Content Security Policy is enabled by default, recommend while testing to comment out that line and use the report line above to test your configuraiton and address in the policy else content may not load. This is an important security header.
# The server is configured for high security by default, but there is work to be done for further hardening.

#Note: the postgres databse is not being used at this time and does not have a certificate to run in a secure configuration over network. Sockets could be used in place of network for single server deployment, but that is not yet developed.

###### END Current manual process from fresh repo ######

### TODO for Script in order it should to execute config ###
# TODO ASK if this is a local config, dev deployment, production deployment to automate system config
# TODO build config file for nginx ie ask for install domain
# TODO build config features to spin up part of ARCS

### initializes the config files for local, testing, staging, and production
# TODO

# TODO run basic security heuristics for config of DNS and certificate ie run observatory.mozilla.org or similar


# TODO add docker build - spin-up and down controls etc
# TODO add PATH commands for easy control ie spin up, backup
# TODO ask for user to create the database username and password
# TODO set directory structure permissions

# TODO ask if user would like to test their server build else display the command to start the system - only need this script on first run
## this initializes a build of the docker-compose and generates the LetsEncrypt certificates only needed on first install to generate a certficate
# sudo ./init-letsencrypt.sh
