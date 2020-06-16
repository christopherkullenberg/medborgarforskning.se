#Directory: ArcsCore-Top
#File: README.md
#Codename: KunsapSkelett
#Version: 0.1
#Developers: Jonathan Brier | Christopher Kullenberg
#Developers email: jonathan.brier@gu.se | christopher.kullenberg@gu.se
#Description: This is an overview README which provides an orientation to the  
# directory structure and reason for the design. The following folders are meant
# to operate in an independent assembly. The focus is on generation of a
# container per component. Together these can be selected via the setup script
# to fit the needs of the implementation. The current design approach follows a
# standard URL naming structure which allows for isolation and independent
# design following a Unix style do one thing and do it well. Thus allowing for
# future components to be integrated using different technologies that the
# community identifies as better suited for the platform. This is designed not
# to dictate what technologies are used, but create a system that is responsive
# to the community's needs.

#Site Structure: Each folder has an expanded README to explain their extent example URL: https://arcs.se/
# ARCSCore-Cms (default URLs):
#    Index - https://arcs.se/en/
#    Blog  - https://arcs.se/en/blog/YYYY/MM/
#    Press Releases / News - https://arcs.se/en/
#    Organization Landing Pages - https://arcs.se/en/org/
# ARCSCore-Foum:
#    Index - https://forum.arcs.se/en/
#    Threads - https://forum.arcs.se/en/
# ARCSCore-Outputs:
#    Index - https://outputs.arcs.se/en/
# ARCSCore-ProjectsData:
#    Index - https://projects.arcs.se/en/
# ARCSCore-Search:
#    Index - https://search.arcs.se/?=
# ARCSPlus-ContinousIntegration
#    Index - https://ci.arcs.se/en/
# ArcsPlus-Translate:
#    Index - https://translate.arcs.se/

#Release Versioning Numbering: x.x.x-buildhash
# Major Release x.0.0.0-buildhash
# Minor Release 0.x.0.0-buildhash
# BugOnlyFix Release 0.0.x-buildhash

#Django Projects Workflow
#Master:
#Branch: Features and User Development Branches
# example UserFeature branch: jonathanbrier_FeatureName
# example Release Branch: ArcsRelease/Version in form of ArcsRelease/1.0.0
