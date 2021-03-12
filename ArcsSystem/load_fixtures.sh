#!/bin/bash
echo Loading fixtures, this may take a moment...

#python manage.py loaddata db.xml




#echo 1. Loading organizations...
#python manage.py loaddata organizations/fixtures/organizations.xml
#echo Organizations loaded

#echo 2. Loading Projects and keyword lines... this one is big....
#python manage.py loaddata projects/fixtures/projects.xml
#echo Projects and Keyword lines fixtures loaded

#echo 3. Loading keywords and publications... this one is big....
#python manage.py loaddata publications/fixtures/publications.xml
#echo Publications fixtures loaded

echo 4. Loading workpackages...
python manage.py loaddata workpackages/fixtures/workpackages.xml
echo Workpackages fixtures loaded!

echo 5. Loading staticpages...
python manage.py loaddata staticpages/fixtures/staticpages.xml
echo Staticpages fixtures loaded




echo Done. Fixtures loaded [unless you saw errors].
