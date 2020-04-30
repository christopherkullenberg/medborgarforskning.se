#
# File Name: README.md
# Description: provide the overview of the ARCSCore project
# Author: Jonathan Brier & Christopher Kullenberg
#

# medborgarforskning.se
Welcome to the [medborgarforskning.se](https://medborgarforskning.se) Documentation! This is the domain to use anywhere the documentation mentions domain.

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

## Translation
Translation is integrated with Django core. Translations occur in templates from the use of {% trans %} where no variable is used or {% blocktrans %} {% endblocktrans %} where the terms and variables would be places between. Each template must include {% load i18n %} at the top of the template to activate translation of the content within the template. More on this can be read about in the Django translation page. https://docs.djangoproject.com/en/2.2/topics/i18n/translation/

## System Architecture
ARCS is build to be a series of containers which host each component.

## Repository Structure
./
├── .git/
│   ├──
│	  └── directoryexample/
├── Arcs/
│   ├──
│	  └──
├── ArcsSystem/
│   ├──
│   └── .../
├── install.sh
└── README.md

# How to Install and Setup an instance of ARCS
## Docker setup

**Prerequisites**
* Docker version 1.13.1, build b2f74b2/1.13.1 - as this is what the RHEL 7 has by default.
* Ansible...
* Domain w/DNS access

# Email Addresses
# list of standard emails to consider https://tools.ietf.org/html/rfc2142
1. webmaster@domain # This email is the primary email to alert the admin of the site of issues.
2. abuse@domain # This email is presented as an option to report inappropriate content.
3. security@domain # This is one of the options presented in the security.txt file to report a security issue found with the site or send notice to users.
4. www@domain # alias of webmaster@domain as stated in rfc2142
# additional emails for this platform
1. info@domain
2. aggregatemail@domain # This email is used by the DMARC record to report aggregate spam emails.
3. forensicmail@domain # This email is used by the DMARC record to report details of the spam emails not in aggregate.



# Domain DNS configuration
- The following domain records should be configured
1. A record and AAAA record - for your server's IP address - ipv4 and ipv6
2. CNAME records for the domain Name
- dev.domain - development domain
- domain - primary Domain
- www -
3. (recommended) CAA record - to state which certificate authorities should be allowed to issue certificates.
- 0 issue "letsencrypt.org" # The platform by default is configured for letsencrypt a trusted free certificate authority.
- 0 iodef "mailto:--replacwithyouremail--" # Email of person to be notified
4. SFP record - authorizes which servers should be able to send email on behalf of the domain. https://tools.ietf.org/html/rfc7208 There are tools available to assist in configuring for your domain.
5. TXT record - plain text record in the DNS
- (recommended) DKIM entry - email handling cryptographic key - will improve your email delivery. Requires coordination with the email provider who will generate the key to enter in the DNS.
- (recommended) DMARC entry - depends on implementing DKIM and SPF - email handling for the emails from your domain and in this configuration the subdomains - improves email delivery. More info at https://dmarc.org/
--  v=DMARC1; p=none; rua=mailto:aggregatemail@domain; ruf=mailto:forensicmail@domain; sp=quarantine; fo=1:d:s
6. DNSSEC - hopefully your DNS provider has this enabled by default, but it is important to maintaining the integrity of the domain resolving to your server.


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


# Merge process

``git checkout master`` 
``git pull origin master``
``git merge test``
``git push origin master`` 



