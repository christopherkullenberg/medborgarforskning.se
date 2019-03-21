from flask import Flask, flash, redirect, render_template
from flask import request, session, abort
import sqlite3

# Database structure:
# CREATE TABLE projects(id INTEGER PRIMARY KEY, name TEXT, datecreated TEXT, 
#                       numberofparticipants INT, keywords TEXT);

app = Flask(__name__)


@app.route("/")
def root():
    '''This serves the main landing page and presents a limited number of
    projects from the database'''
    db = sqlite3.connect('testdb.sqlite3')
    cursor = db.cursor()
    dbquery = cursor.execute('SELECT * FROM projects ORDER BY \
                              datecreated LIMIT 20;')
    selectionresults = {}
    for d in dbquery:
        selectionresults[d[1]] = d[4]
    return render_template("index.html", 
                           result = selectionresults, 
                           selection = "all forskning"
                           )
    db.close()
    

@app.route("/<string:query>/") # use this for building APO web function
def query(query):
    result = {'Projektnamn': query}
    return render_template('index.html', result = result)


@app.route('/result',methods = ['POST', 'GET'])
def result():
    '''This selects projects from the main select dropdowns and dynamically
    updates the landing page with the results'''
    if request.method == 'POST':
        selected = request.form
        db = sqlite3.connect('testdb.sqlite3')
        cursor = db.cursor()
        dbquery = cursor.execute('SELECT * FROM projects WHERE keywords == "' +
                                 selected["typeofproject"] + '";') 
        selectionresults = {}
        for d in dbquery:
            selectionresults[d[1]] = d[4]
        return render_template("index.html", 
                               result = selectionresults, 
                               selection = selected['typeofproject']
                               )
        db.close()
    
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
        selectionresults = {}
        for d in dbquery:
            selectionresults[d[1]] = d[4]
            print(d)
        return render_template("index.html",
                               result = selectionresults,
                               selection = "baserat på sökord"
                               )
        db.close()


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
