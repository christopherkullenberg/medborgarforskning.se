#!/bin/bash
echo Loading fixtures, this may take a moment...


echo Loading keyword lines... this one is big....
python manage.py loaddata projects/fixtures/projects.xml
echo Keyword lines fixtures loaded




echo Loading keywords and publications... this one is big....
python manage.py loaddata publications/fixtures/publications.xml
echo Publications fixtures loaded

echo Loading workpackages... 
python manage.py loaddata workpackages/fixtures/workpackages.xml
echo Workpackages fixtures loaded!




echo Loading organizations...
python manage.py loaddata organizations/fixtures/organizations.xml
echo Organizations fixtures loaded

echo Loading staticpages...
python manage.py loaddata staticpages/fixtures/staticpages.json
echo Staticpages fixtures loaded



echo Done. Fixtures loaded [unless you saw errors].
