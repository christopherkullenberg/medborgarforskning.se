#!/bin/bash

#Directory: Arcs-Top
#File: Setup.sh
#Codename: MasterShell
#Version: 0.1
#Developers: Jonathan Brier | Christopher Kullenberg
#Developers email: jonathan.brier@gu.se | christopher.kullenberg@gu.se
#Description: basic init script to check for system dependencies and
#               walk a user through a configuration file build.

# TODO Check for Parameters being passed handle accordingly - one paramter only.
## TODO --config-file-only Skip user prompts relying on pre-configured SetupConfig.txt
## TODO --uninstall Remove all files, directories, databases... non-recoverable.
## TODO --checkinstall Perform check if all install dependencies are found and
##                       consistent with current config else warn of mismatch.


# TODO Ask if this is a local config, dev deployment, production deployment to automate system config
# TODO identify and set base hardware requirements check. Verify installation
#        system has met a minimum free storage and memory value. Warn if not.
#        TODO rerun after componets are selected with refined paramters to those
#               specified in the selection. Throw warning, do not recommend if
#               continuing if the minimum is not met.


# TODO Check for base package dependencies:
# TODO Check for Docker installation and version (command: docker version)
#        ie Check OS type "cat /etc/os-release", if fail note linux depency
#        point to follow https://docs.docker.com/install/
# TODO Check for python 3.x, if fail. (do we really care at host level?)

# TODO Check for previous installation of ARCS, if found warn, offer
#        clean install = uninstall then runs again or new direcotry.
# TODO Check for completed config file:
#        if exists, but no --config-file-only parameter check config via prompts
#        if does not exist or only defaults, build config file via prompts



## ConfigFile Generator and Validator
# TODO build config file
# Instance="Dev"

# TODO building config file for nginx ie ask for:
# DefaultDomain ="medborgarforskning.se"
# HostPort="443"
# RequiredPort="80"

# TODO identify certificates location (if not in implementation standard folder)
# CertPath="/certificates"

# TODO prompt for which ArcsSystem componets to enable when spinning up the
#        ARCS Instance.
#   Options:
#     all - spin up all images
#     ArcsCore - Spin up only the ArcsCore images.
#     ArcsPlus[ArcsCore,] - Spin up the ArcsCore imagages and the selected
#                             additional ArcsPlus components as named.
# ArcsSystemComponents="all"


# TODO ask for user to enter an existing database username and password
#        store in secrets else generate the database name and password.

# TODO set directory structure permissions

# TODO Write the config file and Secrets to appropriate location. Secrets file
#        should be in the .gitignore file
