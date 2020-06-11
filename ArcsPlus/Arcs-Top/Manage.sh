#!/bin/bash

#Directory: Arcs-Top
#File: Manage.sh
#Codename: MasterControl
#Version: 0.1
#Developers: Jonathan Brier | Christopher Kullenberg
#Developers email: jonathan.brier@gu.se | christopher.kullenberg@gu.se
#Description: script to simplify controls to manage spinup and configuration

# TODO Check for Parameters being passed handle accordingly - one paramter only.
## TODO --securitycheckup Run suite of checks for configuration based on testing
##                          heuristics suite.
## TODO --help Display paramters as options and help docuementation text
## TODO --man Same function as --help
## TODO --reconfigure Safely enable or disable different ArcsSystemComponents.
##                      Currently the implementation focus is all active.


# TODO handle --reconfigure Smooth transition of selection of ArcsSystem
#                             componets.
# TODO Check current configuration ie look at ArcsSystemComponents
# TODO Display current configuration
# TODO Prompt for New Configuration Option:
#     all - spin up all images
#     ArcsCore - Spin up only the ArcsCore images.
#     ArcsPlus[ArcsCore,] - Spin up the ArcsCore imagages and the selected
#                             additional ArcsPlus components as named.
# TODO if configuration is adding a new component. Do it, should be safe.
# TODO if configuration is removing a component or multiple componets. Run test
#        if ArcsSystem code is up to date and if not prompt to read changelog
#        for any recent bug fixes related to removing a component and ask if
#        they have a backup of their database(s) "just in case".

# TODO add docker build - spin-up and down controls etc

# TODO spin up of the instance based on the config file.
# TODO build docker-compose file from config file.
# TODO how to start the project docker-compose up --build


# TODO add PATH commands for:
# --spin-up
# --spin-down
# --backup databases

# TODO run basic security heuristics for config of DNS and certificate ie run observatory.mozilla.org or similar
