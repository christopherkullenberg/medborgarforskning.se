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
