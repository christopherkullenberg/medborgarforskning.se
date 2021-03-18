#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import json
import csv
from xml.sax.saxutils import escape
import requests
import flashtext
from collections import Counter
keyword_processor = flashtext.KeywordProcessor()


#########################
### Generic functions ###
#########################

def replaceslash(keyword):
    if "/" in keyword:
        return keyword.replace("/", "&amp;")
    else:
        return keyword

def remoteimage(value):
    remoteurl = re.sub('\/media\/media\/',
                        '/media/', value)
    return remoteurl

def autokeywordize(datadict):
    #newdatadict = {}
    for k, v in datadict.items():
        #print(v[7].split("; "))
        #print(v[7])
        if len(v[7]) < 1 or v[7] == "_cited_":
            autokeywords = "AUTO; "
            keywords_found = keyword_processor.extract_keywords(k + v[6])
            for c in Counter(keywords_found).most_common(5):
                autokeywords += c[0] + "; "
            datadict[k][7] = autokeywords
        #else:
        #    autokeywords = "AUTO; "
        #    keywords_found = keyword_processor.extract_keywords(k + v[6])
        #    for c in Counter(keywords_found).most_common(5):
        #        autokeywords += c[0] + "; "
        #    datadict[k][7] += autokeywords



    return datadict

#########################
### Data input        ###
#########################

def parsecsv():
    datadict = {}
    with open('publications/ARCSLiterature.csv', 'r') as thefile:
        data = csv.DictReader(thefile, delimiter=',', quotechar='"')
        #keywordlist = []

        for row in data:
            if escape(row['Title']) not in datadict:
                datadict[row['Title']] = [row['Author'],
                                          row['Publication Year'],
                                          row['Publication Title'],
                                          row['Issue'],
                                          row['Volume'],
                                          row['DOI'],
                                          row['Abstract Note'],
                                          row['Manual Tags'],
                                          ]
                #for kw in row['Manual Tags'].split('; '):
                    #clean_kw = escape(kw).lower().strip()
                    #if clean_kw not in keywordlist:
                        #keywordlist.append(clean_kw)
            else:
                continue




        #print(keywordlist)
        return autokeywordize(datadict)

def parseEUprojects():
    response = requests.get("https://eu-citizen.science/api/projects/")
    print("EU API Responded:", response.status_code)
    datadict = {}
    for project in response.json():
        if escape(project['name']) not in datadict:
            datadict[project['name']] = [project['aim'],
                             project['keywords'],
                             project['topic'],
                             project['url'],
                             project['image1'],
                             project['country'],
                             project['dateCreated'],
                             project['start_date'],
                             project['end_date'],
                             project['latitude'],
                             project['longitude'],
                             project['status'],
                             project['mainOrganisation'],
                            ]
        else:
                continue
    return datadict

def makeQdict():
    wikiQdict = {}
    with open('publications/keyword_wikiQs.csv', 'r') as qfile:
        data = csv.DictReader(qfile, delimiter=',', quotechar='"')
        for d in data:
            wikiQdict[d["keyword"]] = d["Q"][1:]
    return wikiQdict

def makesummarydict():
    summarydict = {}
    with open("publications/wikipediasummaryofkeywords.csv", "r") as sumfile:
        data = csv.DictReader(sumfile, delimiter=',', quotechar='"')
        for d in data:
            summarydict[d["keyword"]] = d["summary"]
    return summarydict


####################################
### Transformation functions     ###
####################################



def makekeyworddict():
    keyworddict = {}
    counter = 0
    for k, v in parsecsv().items():
        #add "manual tags"
        keywordlist = v[7].split("; ")
        for x in keywordlist:
            loweredkeyword = replaceslash(escape(x.lower()))
            if len(loweredkeyword) > 1:
                if loweredkeyword not in keyworddict:
                    #print(loweredkeyword)
                    keyworddict[loweredkeyword] = counter
                    counter += 1
        # add autokeywords
        keywords_found = keyword_processor.extract_keywords(k + v[6])
        for c in Counter(keywords_found).most_common(5):
            if c[0] not in keyworddict:
                keyworddict[c[0]] = counter
                counter += 1
    print("Publication keywords: ", str(counter))

    for k, v in parseEUprojects().items():
        for key in v[1]:
            loweredpkeyword = replaceslash(escape(key['keyword'].lower()))
            #print(loweredpkeyword)
            if len(loweredpkeyword) > 1:
                if loweredpkeyword not in keyworddict:
                    #print(loweredkeyword)
                    keyworddict[loweredpkeyword] = counter
                    counter += 1
        for t in v[2]:
                loweredtopic = replaceslash(escape(t['topic'].lower()))
                #print(loweredtopic)
                if len(loweredtopic) > 1:
                    if loweredtopic not in keyworddict:
                        keyworddict[loweredtopic] = counter
                        counter += 1
    print("Created dict with", str(counter -1), " keywords")
    return keyworddict



def engliskeywordstofixture():
    print("Writing keywords...")
    keyworddict = makekeyworddict()
    summary = makesummarydict()
    Q = makeQdict()
    for k, v in keyworddict.items():
        xmloutputfile.write('''<object model="projects.keywordeng" pk="''' + str(v) + '''">''')
        xmloutputfile.write('''   <field name="keyword" type="TextField">''' + replaceslash(k) + '''</field>''')
        if k in summary:
            xmloutputfile.write('''   <field name="summary_en" type="CharField">''' + escape(summary[k]) + '''</field>''')
        else:
            pass
        if k in Q:
            xmloutputfile.write('''   <field name="wikidataQ" type="IntegerField">''' + escape(str(Q[k]))+ '''</field>''')
        else:
            pass
        xmloutputfile.write('''</object>''')
    print("Done writing english keywords with summaries and Qs.")



def makekeywordlines():
    swedish_kw_dict = {}
    translation_line_dict = {}
    counter_id_sv = 0
    counter_id_line = 0
    keyworddict = makekeyworddict()
    duplicationchecklist = []
    with open('publications/top500keywordsSVENtranslated.csv', 'r') as thefile:
        data = csv.DictReader(thefile, delimiter=',', )
        for d in data:
            if d["en"] not in duplicationchecklist:
                duplicationchecklist.append(d["en"])
                if len(d["sv"]) > 1:
                    #print(d['sv'], d['en'])
                    # flera översättnigar för samma engelska ord
                    if d["sv"] in swedish_kw_dict:
                        translation_line_dict[counter_id_line] = [swedish_kw_dict[d["sv"]], keyworddict[d["en"].strip()]]
                        counter_id_line += 1
                    # ifall det inte finns
                    else:
                        swedish_kw_dict[d["sv"]] = counter_id_sv
                        translation_line_dict[counter_id_line] = [counter_id_sv, keyworddict[d["en"].strip()]]
                        counter_id_sv += 1
                        counter_id_line += 1
            else:
                print("found duplicate: ", d["en"])
                continue

    #add the rest of the non translated keywords
    #for k, v in keyworddict.items():
    #    if k not in alreadyadded:
    #        swedish_kw_dict[k] = counter_id_sv
    #        translation_line_dict[counter_id_line] = [counter_id_sv, keyworddict[k]]
    #        counter_id_sv += 1
    #        counter_id_line += 1

    #print("Counter id sv: ", str(counter_id_sv))
    #print("Counter id line: ", str(counter_id_line))
    return [swedish_kw_dict, translation_line_dict]

def swedishkeywordstofixture():
    counter = 0
    for k, v in makekeywordlines()[0].items():
        #print(k, v)
        xmloutputfile.write('''<object model="projects.keywordswe" pk="''' + str(v) + '''">''')
        xmloutputfile.write('''   <field name="keyword" type="TextField">''' + replaceslash(escape(k)) + '''</field>''')
        xmloutputfile.write('''</object>''')
        counter += 1
    print("Added ", str(counter), "swedish keyword to fixture")
        # kom ihåg sv , en här lägggs pk till för båda språken

def keywordlinestofixture():
    counter = 0
    for k, v in makekeywordlines()[1].items():
        #if k in swedish_kw_dict:
        #    print(k)
        #if k < 666:
        #print(k,v)
        xmloutputfile.write('''<object model="projects.keywordline" pk="''' + str(k) + '''">''')
        xmloutputfile.write('''   <field name="eng" type="ForeignKey">''' + str(v[1]) + '''</field>''')
        xmloutputfile.write('''   <field name="swe" type="ForeignKey">''' + str(v[0]) + '''</field>''')#
        xmloutputfile.write('''</object>''')
        counter += 1
    print("Added ", str(counter), "keyword lines to fixture")

def kwlookup(kwlist, keyworddict, translation_line_dict):
    kwlookuplist = []
    for k, v in translation_line_dict.items():
        for x in kwlist:
            loweredkeyword = replaceslash(escape(x)).lower() #this needs to be done since we are inputing raw data again.
            #print(loweredkeyword)
            if loweredkeyword in keyworddict:
                if keyworddict[loweredkeyword] == v[1]:
                    kwlookuplist.append(k)
            else:
                continue
    return kwlookuplist

def monolangkwlookup(kwlist, keyworddict, translation_line_dict):
    kwlookuplist = []
    for k, v in translation_line_dict.items():
        for x in kwlist:
            loweredkeyword = replaceslash(escape(x)).lower() #this needs to be done since we are inputing raw data again.
            #print(loweredkeyword)
            if loweredkeyword in keyworddict:
                if keyworddict[loweredkeyword] == v[1]:
                    kwlookuplist.append(v[1])
            else:
                continue
    return kwlookuplist



def publicationstofixture():
    keyworddict = makekeyworddict()
    translation_line_dict = makekeywordlines()[1]
    counter = 0
    for k, v in parsecsv().items():
        #print("in publicationstofixture()",k, v[7])
        if not v[1]: #there must be a publication year
            pass
        else:
            xmloutputfile.write('''<object model="publications.article" pk="''' + str(counter) + '''">\n''')
            xmloutputfile.write('''  <field name="title" type="CharField">''' + escape(k) + '''</field>\n''')
            xmloutputfile.write('''  <field name="title_en" type="CharField">''' + escape(k) + '''</field>\n''')
            xmloutputfile.write('''<field name="abstract" type="CharField">''' + escape(v[6]) + '''</field>\n''')
            xmloutputfile.write('''<field name="abstract_en" type="CharField">''' + escape(v[6]) + '''</field>\n''')
            xmloutputfile.write('''<field name="doi" type="CharField">''' + escape(v[5]) +'''</field>\n''')
            xmloutputfile.write('''<field name="py" type="IntegerField">''' + v[1] + '''</field>\n''')
            xmloutputfile.write('''<field name="authors" type="CharField">''' + escape(v[0]) + '''</field>\n''')
            xmloutputfile.write('''<field name="source" type="CharField">''' + escape(v[2]) + '''</field>\n''')
            xmloutputfile.write('''<field name="volume" type="CharField">''' + v[4] + '''</field>\n''')
            xmloutputfile.write('''<field name="issue" type="CharField">''' + v[3] + '''</field>\n''')
            xmloutputfile.write('''<field name="keywords" rel="ManyToManyRel" to="publications.keyword">\n''')
            # keyword addition
            articlekwlist = v[7].split("; ") # Note: these are raw, so escape, replaceslash and lower is done in kwlookup()
            #print(articlekwlist)
            for pkvalue in monolangkwlookup(articlekwlist, keyworddict, translation_line_dict):
                #print(pkvalue)
                if pkvalue:
                    xmloutputfile.write('''<object pk="''' + str(pkvalue) + '''"></object>"\n''')
                    #print(pkvalue)
            #for a in articlekwlist:
            #    clean_a = replaceslash(escape(a)).lower().strip()
            #    print(clean_a)
            #    for single_clean_a in clean_a:
            #        if single_clean_a in keyworddict:
            #            xmloutputfile.write('''<object pk="''' + str(keyworddict[single_clean_a]) + '''"></object>"\n''')
            #            print(single_clean_a, keyworddict[single_clean_a])


            xmloutputfile.write('''</field>\n''')
            xmloutputfile.write('''</object>\n''')
            counter += 1
    print("Added ", str(counter), "publications to fixture")


def projectstofixture():
    keyworddict = makekeyworddict()
    translation_line_dict = makekeywordlines()[1]
    counter = 0
    for k, v in parseEUprojects().items():
        #print(escape(k))
        xmloutputfile.write('''<object model="projects.projectentry" pk="''' + str(counter) + '''">\n''')
        xmloutputfile.write('''  <field name="date_created" type="DateTimeField">''' + v[6] + '''</field>\n''')
        xmloutputfile.write('''  <field name="date_updated" type="DateTimeField">''' + v[6] + '''</field>\n''')
        xmloutputfile.write('''  <field name="name" type="CharField">''' + escape(k) + '''</field>\n''')
        xmloutputfile.write('''  <field name="aim" type="CharField">''' + escape(v[0]) + '''</field>\n''')
        xmloutputfile.write('''  <field name="country" type="CountryField">''' + escape(v[5]) + '''</field>\n''')
        xmloutputfile.write('''  <field name="latitude" type="DecimalField">''' + v[9] + '''</field>\n''')
        xmloutputfile.write('''  <field name="longitude" type="DecimalField">''' + v[10] + '''</field>\n''')
        xmloutputfile.write('''  <field name="status" type="CharField">''' + str(v[11]['id']) + '''</field>\n''')

        try:
            print(str(v[12]['name']))
            xmloutputfile.write('''  <field name="responsible_party_name" type="CharField">''' + escape(str(v[12]['name'])) + '''</field>\n''')
        except TypeError:
            xmloutputfile.write('''  <field name="responsible_party_name" type="CharField">N/A</field>\n''')

        # Images
        try:
            xmloutputfile.write('''  <field name="image" type="URLField">''' + remoteimage(v[4]) + '''</field>\n''')
        except TypeError:
            xmloutputfile.write('''  <field name="image" type="URLField">''' + "defaultimage" + '''</field>\n''')
        except AttributeError:
            xmloutputfile.write('''  <field name="image" type="URLField">''' + "defaultimage" + '''</field>\n''')
        # URLs (must be something)
        try:
            #print(localimage(v[4]))
            xmloutputfile.write('''  <field name="url" type="URLField">''' + escape(v[3]) + '''</field>\n''')
        except TypeError:
            xmloutputfile.write('''  <field name="image" type="URLField">''' + "http://example.com" + '''</field>\n''')
        except AttributeError:
            xmloutputfile.write('''  <field name="image" type="URLField">''' + "http://example.com" + '''</field>\n''')

        # keywords per project in one list
        keywordlist = []
        for listitem in v[1]:
            keywordlist.append(replaceslash(escape(listitem['keyword'])).lower())
        for listitem in v[2]:
            keywordlist.append(replaceslash(escape(listitem['topic'])).lower())

        # Add keywordlines to projects.
        xmloutputfile.write('''<field name="keyword_lines" rel="ManyToManyRel" to="projects.keywordline">\n''')
        for k in keywordlist:
            if k in keyworddict: # check that the keyword exists
                # Takes the keywordlist and sends it to kwlookup() which returns the keyword line pk.
                for pkvalue in kwlookup([k], keyworddict, translation_line_dict):
                    xmloutputfile.write('''<object pk="''' + str(pkvalue) + '''"></object>\n''')
        xmloutputfile.write('''<object pk="0"></object>\n''') #statically adding "citizen science" to all projects
        xmloutputfile.write('''</field>\n''')
        #finishing object tag for entire project entry
        xmloutputfile.write('''</object>\n''')
        counter += 1
        #print(keyworddict)
    print("Added ", str(counter), "projects to fixture")


##########################################################################################
for k, v in parsecsv().items():
    for kw in v[7].split('; '):
        keyword_processor.add_keyword(escape(kw.strip()))
print("keyword processor fed with publications keywords")

xmloutputfile = open('../keywords/fixtures/keywords.xml', 'w')
xmloutputfile.write('''<?xml version="1.0" encoding="utf-8"?>\n''')
xmloutputfile.write('''<django-objects>\n''')
engliskeywordstofixture()
swedishkeywordstofixture()
keywordlinestofixture()
publicationstofixture()
projectstofixture()
#print(makekeywordlines()[0])
xmloutputfile.write('''</django-objects>''')
xmloutputfile.close()

#############ugly hack to add stuff to keyword lines ##########
def definemissingtranslations(currenttranslationlist):
    with open("untranslatedkeywords.txt", "w") as allkw:
        for k, v in makekeyworddict().items():
            if k not in currenttranslationlist:
                allkw.write(replaceslash(k).lower().strip() + "\n")

currenttranslationlist = []
with open('publications/top500keywordsSVENtranslated.csv', 'r') as thefile:
    data = csv.DictReader(thefile, delimiter=',', )
    for d in data:
        currenttranslationlist.append(escape(replaceslash(d["en"].lower().strip())))

definemissingtranslations(currenttranslationlist)

############# /ugly hack to add stuff to keyword lines ########

print("keywords/fixtures/keywords.xml was written.")
