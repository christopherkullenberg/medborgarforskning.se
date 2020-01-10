from flask import Flask, flash, redirect, render_template
from flask import request, session, abort
import sqlite3
import json


app = Flask(__name__)

############################
# API functions and routes #
############################

def apisearchprojects(searchstring, orderby, order):
    ''' Searches the project database and returns
    the query results and the cursor'''
    db = sqlite3.connect('testdb.sqlite3')
    cursor = db.cursor()
    dbquery = cursor.execute('SELECT * FROM projects WHERE (name LIKE "%'
                             + searchstring + '%" OR keywords LIKE "%' 
                             + searchstring + '%") ORDER BY ' 
                             + orderby.title() 
                             + ' ' + order.upper() + ';')
    print(dbquery)
    return dbquery, cursor

def apisearchliterature(searchstring, orderby, order):
    ''' Searches the literature database and returns
    the query results and the cursor'''
    db = sqlite3.connect("ARCSLiterature.sqlite3")
    cursor = db.cursor()
    dbquery = cursor.execute('SELECT * FROM\
                              bibliography WHERE Keywords LIKE "%' 
                              + searchstring + '%" OR Author LIKE "%'
                              + searchstring + '%" OR Abstract LIKE "%'    
                              + searchstring + '%" OR Title LIKE "%'
                              + searchstring + '%" ORDER BY ' + orderby.title()
                              + ' ' + order.upper() + ';')
    return dbquery, cursor
 
@app.route('''/api/database=<string:query>&searchstring=<string:query2>&orderby=<string:query3>&order=<string:query4>''')
# Route for API URL pattern
# Example queries: 
# http://localhost/api/database=projects&searchstring=biologi&orderby=name&order=desc
# http://localhost/api/database=literature&searchstring=birds&orderby=year&order=asc 
def query(query, query2, query3, query4):
    if query == "projects":
        result = apisearchprojects(query2, query3, query4)[0]
        cursor = apisearchprojects(query2, query3, query4)[1]
        items = [dict(zip([key[0] for key in cursor.description], row)) 
                 for row in result]
        return json.dumps({'items': items}, ensure_ascii=False).encode('utf8')
    
    elif query == "literature":
        result = apisearchliterature(query2, query3, query4)[0]
        cursor = apisearchliterature(query2, query3, query4)[1]
        items = [dict(zip([key[0] for key in cursor.description], row)) 
                 for row in result]
        return json.dumps({'items': items}, ensure_ascii=False).encode('utf8')
    
    
    else:
        datatype = "Error. Datatype must be 'projects' or 'literature'"
        return datatype 


#####################################
# Web frontend functions and routes #
#####################################

def renderresults(dbquery, selection, selectionloc):
    '''This function renders the results of CS projects based on 
    the index.html /template. It is used by root(), result() and 
    searchprojects(), which share a common data structure.'''
    selectionresults = {}
    for d in dbquery:
        # add to value list whatever you need on the frontend from the db.
        selectionresults[d[1]] = [d[4], d[6], d[7], d[8], d[5]]
    print(selectionresults) # for debugging to see what is in dict.
    return render_template("index.html",
                           result = selectionresults,
                           selection = selection,
                           selectionloc = selectionloc
                           )

@app.route("/")
def root():
    '''This serves the main landing page and presents a limited number of
    projects from the database'''
    db = sqlite3.connect('testdb.sqlite3')
    cursor = db.cursor()
    dbquery = cursor.execute('SELECT * FROM projects ORDER BY \
                              datecreated LIMIT 20;')
    selectionresults = {}
    selection = "alla medborgarforsknings"
    selectionloc = "hela Sverige"
    return renderresults(dbquery, selection, selectionloc)
    
@app.route('/medborgarforskning')
def rendermedborgarforskning():
    return render_template('medborgarforskning.html')

@app.route('/startaprojekt')
def renderstartaprojekt():
    return render_template('startaprojekt.html')

@app.route('/om-arcs')
def renderabout():
    return render_template('om_arcs.html')

@app.route('/litteratur', methods = ['POST', 'GET'])
def renderlitteratur():
    #print(literaturequery("civic"))
    results = {"default": "234"}
    litdb = sqlite3.connect('ARCSLiterature.sqlite3')
    cursor = litdb.cursor()
    if request.method == 'POST':
        searchstring = request.form
        orderby = "Year DESC"
        print(searchstring)
        for k, v in searchstring.items():
            if k == "Author":
                orderby = "Author ASC"
        print(orderby)
        results = cursor.execute('SELECT * FROM\
                                  bibliography WHERE Keywords LIKE "%' 
                                  + searchstring['searchliterature'] + '%" OR\
                                  Author LIKE "%'
                                  + searchstring['searchliterature'] + '%" OR\
                                  Abstract LIKE "%'    
                                  + searchstring['searchliterature'] + '%" OR\
                                  Title LIKE "%'
                                  + searchstring['searchliterature'] + '%"\
                                  ORDER BY ' + orderby + ';')
    
    else:
        results = cursor.execute('SELECT * FROM bibliography WHERE Year < 3000\
                                  ORDER BY Year DESC LIMIT 20;')
    return render_template('litteratur.html', 
                           results = results)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    '''This selects projects from the main select dropdowns and dynamically
    updates the landing page with the results. It uses greedy LIKE searches
    to encompass multiple keywords and locations in the DB columns.'''
    if request.method == 'POST':
        selected = request.form
        db = sqlite3.connect('testdb.sqlite3')
        cursor = db.cursor()
        querystring = (selected["typeofproject"], selected["locationofproject"])
        print(querystring) # check the query in debug mode
        if querystring[0] == "alla medborgarforsknings":
            dbquery = cursor.execute('SELECT * FROM projects WHERE location\
                                     LIKE "%' + querystring[1] + '%";')
        else:
            dbquery = cursor.execute('SELECT * FROM projects WHERE keywords\
                                     LIKE "%' + querystring[0] + '%" AND \
                                     location LIKE "%' + querystring[1] + '%";') 
        selection = selected['typeofproject'],
        selectionloc = selected['locationofproject']
        return(renderresults(dbquery, selection[0], selectionloc))
    
@app.route('/search', methods = ['POST', 'GET'])
def searchprojects():
    '''This delivers search query based results and renders them on 
    the landing page.'''
    if request.method == 'POST':
        searchstring = request.form
        print("Search query is " + str(searchstring['searchstring']))
        db = sqlite3.connect('testdb.sqlite3')
        cursor = db.cursor()
        dbquery = cursor.execute('SELECT * FROM projects WHERE (name LIKE "%' 
                                 + searchstring['searchstring'] + 
                                 '%" OR keywords LIKE "%' + 
                                 searchstring['searchstring'] + '%");')
        selection = "baserat på sökord"
        selectionloc = "baserat på sökord"
        return(renderresults(dbquery, selection, selectionloc))




if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
