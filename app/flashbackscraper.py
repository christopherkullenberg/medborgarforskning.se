from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import sys
import datetime
import csv

counter = 1

def parsethread(nexturl):
    print("Scraping", nexturl)
    threadnumber = nexturl[26:]
    postidlist = []
    userlist = []
    datelist = []
    timelist = []
    bodylist = []
    inreplylist = []
    r = requests.get(nexturl)
    print(r)
    html = r.content
    soup = BeautifulSoup(html, "lxml")
    #print(soup)
    postbody = soup.findAll("div", class_="post_message")
    username = soup.findAll("li", class_="dropdown-header")
    heading = soup.findAll("div", class_="post-heading")
    print("Length: " + str(len(postbody)))
    for p in postbody:
        postid = re.findall("(?<=id\=\"post\_message\_).*?(?=\"\>)", str(p), 
                            re.IGNORECASE)
        if postid:
            postidlist.append(postid[0])
    for u in username:
        if u.text == "Ämnesverktyg":
            continue
        else:
            userlist.append(u.text)
    for h in heading:
        yesterday = datetime.date.today() - datetime.timedelta(1)
        todaymatch = re.findall("Idag,\s\d\d\:\d\d", h.text, re.IGNORECASE)
        yesterdaymatch = re.findall("Igår,\s\d\d\:\d\d", h.text, re.IGNORECASE)
        match = re.findall("\d\d\d\d\-\d\d\-\d\d,\s\d\d\:\d\d", h.text, 
                           re.IGNORECASE)
        if todaymatch:
            datelist.append(datetime.date.today())
            #print(datetime.date.today())
            timelist.append(todaymatch[0][6:])
        elif yesterdaymatch:
            datelist.append(yesterday)
            #print(yesterday)
            timelist.append(yesterdaymatch[0][6:])
        elif match:
            datelist.append(match[0][:10])
            print(match[0][:10])
            timelist.append(match[0][12:])
    for p in postbody:
        bodylist.append(p.text)
    for p in postbody:
        match = re.findall("(?<=Ursprungligen postat av ).*", p.text, 
                           re.IGNORECASE)
        if match:
            inreplylist.append(match[0])
        else:
            inreplylist.append("none")

    print(len(postidlist), len(userlist), len(datelist), len(timelist), 
          len(bodylist), len(inreplylist))
    #print(soup)


