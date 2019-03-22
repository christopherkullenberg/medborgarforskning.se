from flask import Flask, flash, redirect, render_template
from flask import request, session, abort
import sqlite3

# Database structure:
# CREATE TABLE projects(id INTEGER PRIMARY KEY, name TEXT, datecreated TEXT, 
#                       numberofparticipants INT, keywords TEXT);

app = Flask(__name__)

def renderresults(dbquery, selection, selectionloc):
    '''This function renders the results of CS projects based on 
    the index.html /template. It is used by root(), result() and 
    searchprojects(), which share a common data structure.'''
    selectionresults = {}
    for d in dbquery:
        selectionresults[d[1]] = [d[4], d[6]]
    print(selectionresults)
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
    return(renderresults(dbquery, selection, selectionloc))
    
@app.route('/medborgarforskning')
def rendermedborgarforskning():
    return render_template('medborgarforskning.html')


@app.route("/<string:query>/") # use this for building APO web function
def query(query):
    result = {'Projektnamn': query}
    return render_template('index.html', result = result)

@app.route('/result',methods = ['POST', 'GET'])
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


# Just and example function
@app.route("/hello")
def hello():
    return "Hello World from Flaskan. Testar att starta om"


# Just an example function
@app.route("/gendercounter/<string:name>/")
def getGender(name):
    import gendercounter
    namnet = gendercounter.from_string(name)
    return str(namnet.genderfrequency())



if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
