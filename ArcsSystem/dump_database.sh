#!/bin/bash

echo "Dumping database to xml file db.xml..."
python manage.py dumpdata --exclude auth.permission --format xml > db.xml
echo "Done! [unless you saw errors]"


