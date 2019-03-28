import csv
import re

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

def literaturequery(query):
    thedata = parsecsv()
    results = {}
    for key, value in thedata.items():
        # make a search in title, abstract, keywords
        regexp = re.findall(query, value[2] + value[6] + value[7], re.IGNORECASE)
        if regexp:
            results[key] = value
            #print(key, value)
        else:
            continue
    return results



