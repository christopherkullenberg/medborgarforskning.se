The basic architecture design of ARCSystem is a name spaced approach to
create a core system that can be enabled which have features that can be turnkey
and not required much technical knowledge to deploy and maintain.

The following are the list of apps and functionalities which they are focused.

1. Project Database
The project database is designed to act as a bounded scope database for
curating projects based on the organization running the platform. The initial
project ARCS defines the bounds for curation as projects of Sweden while
integrating with other existing databases to search globally for projects of
interest for the researchers in Sweden.

This relies upon the PPSR-Core PMM model which is collaboratively maintained and
developed by the Data and Metadata Working group collaboration of the
Citizen Science Association (CSA), European Citizen Science Association (ECSA),
and Australian Citizen Science Association (ACSA) and the growing number of
associations. PPSR-Core standards are published at
https://github.com/CitSciAssoc/DMWG-PPSR-Core

The current model and exchange focused on a trusted network of databases, but
does have room for improvement in the integrity of the data exchange. This is
an area for future development.


2. People Database
The initial scope of the people database are one to create a public profile for
person running citizen science projects and researchers who are interested in
citizen science to identify their interests and help find others with specific
expertise or shared / complementary interest(s).


3. Publications Database
The initial scope of this are the papers collected by the

Future development is focused on an expanded tagging of publications related
to citizen science starting with peer reviewed papers and books.


4. Resources Database -
The initial scope of this is to support the curated works of the
ARCS Workpackages focused on identifying and synthesizing the best practices and
information for researchers to understand citizen science and provide an
orientation to the methods and practices.


5. Static Pages App
This app functions as a basic content management system (CMS) for the site
allowing for content focused pages


6. Blog App
Provide a basic blog for communications from the platform to the public.
