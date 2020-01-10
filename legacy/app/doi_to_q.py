#/usr/bin/python3
import sys
print(sys.version)
import sqlite3
import urllib3
from scholia import query


test = query.doi_to_qs("10.1371/journal.pone.0147152")

print(test)
import re



db = sqlite3.connect("ARCSLiterature.sqlite3")
cursor = db.cursor()
dbquery = cursor.execute('SELECT DOI, Keywords, Title FROM bibliography;')


for d in dbquery:
    for x in d:
        match = re.findall("citizen science", x, re.IGNORECASE)
        if match:
            print("---" * 20)
            print("TITLE:", d[2])
            print("DOI:", d[0])
            print("KEYWORDS:", d[1]) 
            print("HAS Q: ", query.doi_to_qs(d[0]))


#for d in dbquery:
#    print(query.doi_to_qs(d[0]))


