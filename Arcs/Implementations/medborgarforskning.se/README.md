#Directory: Arcs-Top
#File: README.md
#Codename: ArcsPrime
#Version: 0.1
#Developers: Jonathan Brier | Christopher Kullenberg
#Developers email: jonathan.brier@gu.se | christopher.kullenberg@gu.se
#Description: This document provides a overview of the technical and design of
#the medborgarforskning.se implementation.

# medborgarforskning.se
Welcome to the [medborgarforskning.se](https://medborgarforskning.se) Documentation!

Medborgarforskning.se is a portal for connecting citizen science researchers and publics in Sweden and elsewhere.

This projects is part the ARCS project, which is a collaboration project between the University of Gothenburg, the Swedish University of Agricultural Sciences, Umeå University and the non-profit organization VA (Public & Science).


# Overview

_The following documentation is under development and will be updated before launch in May 2020._

## What is this medborarforskning portal?

### Scope of medborarforskning
The primary focus is to serve researchers and the public in providing an orientation and understanding of what citizen science is, what citizen science is being conducted in Sweden, and how researchers and the public can connect to conduct citizen science.

The portal is designed to be a comprehensive inventory of the citizen science conducted by researchers and the publics in Sweden and allow for discovery of projects that are able to be conducted in Sweden that are hosted by external researchers. The portal aims to facilitate an orientation to connect researchers with best considerations and resources for the practice of citizen science and to help researchers and the public find ways to do citizen science.

The content hosted on this site will be available in Swedish and English,  

#### Snippet of Content
* Projects conducted by researchers and the publics of Sweden (inclusive of projects receiving funding from Sweden if hosted elsewhere or part of a larger collaboration)
* Search of projects that provide Sweden as a scope of where their activities are being conducted
* Publications related to citizen science
* Design, administrative, ethical, etc considerations when implementing and joining a project
* Links to external resources and organizations for the practices in citizen science

## Areas to be Documented:
* Getting Started with Dev and Configuration
* Site Architecture
* Databases and Design
The project list will follow and extend upon the PPSR-Core standard for
* Permission and Roles Structure
* Design Style Guide
* Coding Style Guide
* Process for changes impacting GDPR protected data, Terms of Service, Privacy, Cookies, Tracking, and processing of information about individuals.
* Community Guidelines

## Project Vocabulary and Terms
* Project - refers to the top level of the Django framework - the initialized collection of components and apps. Also referred to the collection of all the files in the Repo.  
* App - is a term used in Django to refer to the features of the site that perform a function. ie to handle pages there could be a page app. For a post there could be a post app.
* Component - refers to a part of the ARCSCore Project that can be run independent of other major sections of the platform.
*

# Design and Decisions
## Coding Style
Python Core Style - PEP8 https://pep8.org/
Django Style - https://docs.djangoproject.com/en/2.2/internals/contributing/writing-code/coding-style/


## System Architecture
ARCS is build to be a series of containers which host each component.

# How to Install and Setup an instance of ARCS
## Docker setup

**Prerequisites**
* Docker version 1.13.1, build b2f74b2/1.13.1 - as this is what the RHEL 7 has by default.
* Ansible...

# First run and controlling the containers
## First Run Only
The first run will setup the docker images

Commands:
1. Copy the Git repo to a directory which will act as the base of your server. We assume you are installing in a Linux environment.
2. install.sh
Follow the prompts from the script to configure your first installation.

## Ongoing
2.

## Programming and Application Environment
LTS versions of software are selected for longer support periods and ease of maintenance by the community.

The Docker environment consists of the following dependencies:

* Ubuntu 18.04 LTS
* Django 2.2.x
* Python 3.x
* Postgresql

* Virtual Environment



For full requirements, see the ``requirements.txt`` file.

# Continuous Testing an Quality Assurance
The configuration integrates a testing process in with git and spin-up to avoid issues in production.

1. Continuous Integrated Testing
