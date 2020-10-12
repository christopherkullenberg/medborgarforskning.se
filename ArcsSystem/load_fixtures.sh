#!/bin/bash
echo Loading fixtures, this may take a moment...

python manage.py loaddata workpackages/fixtures/workpackages.xml
echo Workpackages fixtures loaded!

python manage.py loaddata publications/fixtures/publications.xml
echo Publications fixtures loaded

python manage.py loaddata organizations/fixtures/organizations.xml
echo Organizations fixtures loaded


echo Done. Fixtures loaded [unless you saw errors].
