# medborgarforskning.se
Welcome to the [medborgarforskning.se](https://medborgarforskning.se) Documentation! This is the domain to use anywhere the documentation mentions domain.

Medborgarforskning.se is a portal for connecting citizen science researchers and publics in Sweden and elsewhere. The current code in this repository is in development.

This projects is part of the ARCS project, which is a collaboration project between the University of Gothenburg, the Swedish University of Agricultural Sciences, Umeå University and the non-profit organization VA (Public & Science).

## Contributors (alphabetically ordered)

* [Jonathan Brier](https://github.com/brierjon)
* [Aram Karimi](https://github.com/AramKarimi)
* [Isak Karlstens](https://github.com/AvoCod3o)
* [Christopher Kullenberg](https://github.com/christopherkullenberg)



# Overview

### Scope of medborgarforskning.se and the ArcsSystem
The primary focus is to serve researchers and the public in providing an orientation and understanding of what citizen science is, what citizen science is being conducted in Sweden, and how researchers and the public can connect to conduct citizen science.

The portal is designed to be a comprehensive inventory of the citizen science conducted by researchers and the publics in Sweden and allow for discovery of projects that are able to be conducted in Sweden that are hosted by external researchers. The portal aims to facilitate an orientation to connect researchers with best considerations and resources for the practice of citizen science and to help researchers and the public find ways to do citizen science.

The content hosted on this site will be available in Swedish and English,  

#### Some features
* Projects conducted by researchers and the publics of Sweden (inclusive of projects receiving funding from Sweden if hosted elsewhere or part of a larger collaboration)
* Search of projects that provide Sweden as a scope of where their activities are being conducted
* Publications related to citizen science and comprehensive keyword discovery
* Design, administrative, ethical, etc considerations when implementing and joining a project
* Links to external resources and organizations for the practices in citizen science

## Translation
Translation is integrated with Django core. Translations occur in templates from the use of {% trans %} where no variable is used or {% blocktrans %} {% endblocktrans %} where the terms and variables would be places between. Each template must include {% load i18n %} at the top of the template to activate translation of the content within the template. More on this can be read about in the Django translation page. https://docs.djangoproject.com/en/2.2/topics/i18n/translation/

## System Architecture
ARCS is built to be a series of containers which host each component.


## Domain DNS configuration
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

## Docker setup

**Prerequisites**
* Docker version 1.13.1, build b2f74b2/1.13.1 - as this is what the RHEL 7 has by default.
* Domain w/DNS access



### First run and controlling the containers
The first run will setup the docker images:

Commands:

1. Copy the Git repo to a directory which will act as the base of your server. We assume you are installing in a Linux environment. If you have not made any changes to the nginx configuration, you can leave this directory as it was in previous
setups. Usually, a new version of the site only requires the code in ``ArcsSystem`` to be copied over.

2. Check that ``docker-compose.yaml`` and ``ArcsSystem/Dockerfile`` are correct.

3. If you have added or subtracted python modules using pipenv, you should create a new requirements file by running ``pipenv lock -r > requirements.txt`` and copy it over. (The docker script uses pip rather than pipenv to simplify a system wide environment.)

4. If you want to clear out old stuff, you can run ``docker system prune -a`` and ``docker rm -f ARCS-PG-DB ARCSCore LetsEncrypt ARCServer``. **WARNING:** This destroys all previous data.

5. Now you can run ``docker-compose up --build``

6. Once the containers are spun up, you will need to perform the migrations and stuff. Find the ARCServer container ID with  ``docker ps`` then get shell access to it with ``docker exec -it XXXXXXXXX bash``.

7. From inside of the ARCSystem container run:

    a) ``sh clear_migrations.sh`` -- **WARNING:** Only for a completely empty database!

    b) ``python manage.py makemigrations``

    c) ``python manage.py migrate``

    d) ``python manage.py createsuperuser``

    e) ``sh load_fixtures.sh``

8. Now it should work.



# Merge process

``git checkout master``
``git pull origin master``
``git merge test``
``git push origin master``
