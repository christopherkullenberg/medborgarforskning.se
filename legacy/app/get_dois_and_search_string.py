#/usr/bin/python3
import sys
print(sys.version)
import sqlite3
import urllib3
import re



db = sqlite3.connect("ARCSLiterature.sqlite3")
cursor = db.cursor()
dbquery = cursor.execute('SELECT DOI FROM bibliography;')

counter = 0


with open("dois_in_search_syntax.txt", "w") as outfile:
    for d in dbquery:
        if d[0]:
            outfile.write('"' + d[0] + '" OR \n')
            counter += 1

print("Wrote " + str(counter) + " DOIs.")


