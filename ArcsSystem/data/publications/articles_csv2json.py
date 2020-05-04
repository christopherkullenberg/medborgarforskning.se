import re
import sys
import json
import csv

def parsecsv():
    with open('ARCSLiterature.csv', 'r') as thefile:
        data = csv.DictReader(thefile, delimiter=',', quotechar='"')
        datadict = {}
        for row in data:
            if row['Title'] not in datadict:

                datadict[row['Title']] = [row['Author'],
                                          row['Publication Year'],
                                          row['Publication Title'],
                                          row['Issue'],
                                          row['Volume'],
                                          row['DOI'],
                                          row['Abstract Note'],
                                          row['Manual Tags']
                                          ]

            else:
                continue
        return datadict

pk = 1

valueslist = []

with open('publications.yaml', 'w') as f:
    for k, v in parsecsv().items():

        title = k.replace('"', ' ')
        authors = v[0].replace('"', ' ')
        py = v[1]
        source = v[2].replace('"', ' ')
        issue = v[3]
        volume = v[4]
        DOI = v[5]
        abstract = v[6].replace('"', ' ')
        keywords = v[7].replace('"', ' ')

        f.write('- model: publications.Article\n')
        f.write('  pk: ' + str(pk) + "\n")
        f.write('  fields:\n')
        f.write('    title: "' + title.replace(':', ' ') + '"\n')
        f.write('    keywords: "' + keywords + '"\n')
        f.write('    abstract: "' + abstract + '"\n')
        f.write('    doi: ' + DOI + "\n")
        f.write('    py: ' + py + "\n")
        f.write('    authors: "' + authors + '"\n')
        f.write('    source: "' + source + '"\n')
        f.write('    volume: ' + volume + '\n')
        f.write('    issue: ' + issue + '\n')

        pk += 1
        if pk > 10:
            break
