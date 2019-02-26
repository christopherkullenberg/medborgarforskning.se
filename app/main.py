from flask import Flask, flash, redirect, render_template, request, session, abort

import sqlite3
# CREATE TABLE projects(id INTEGER PRIMARY KEY, name TEXT, datecreated TEXT, numberofparticipants INT, keywords TEXT);

app = Flask(__name__)


@app.route("/")
def root():
    selected = {'typeofproject': 'all forskning'}
    return render_template("index.html", 
                           result = selected, 
                           selection = selected['typeofproject'])

@app.route("/<string:query>/") # use this for search function
def query(query):
    result = {'Projektnamn': query}
    return render_template('index.html', result = result)


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        selected = request.form
        db = sqlite3.connect('testdb.sqlite3')
        cursor = db.cursor()
        dbquery = cursor.execute('SELECT * FROM projects WHERE keywords == "' +
                                 selected["typeofproject"] + '";') 
        selectionresults = {}
        for d in dbquery:
            selectionresults[d[1]] = d[4]
        
        print(selected['typeofproject'])
        print(selectionresults)
        return render_template("index.html", 
                               result = selectionresults, 
                               selection = selected['typeofproject']
                               )
        db.close()
    



@app.route("/hello")
def hello():
    return "Hello World from Flaskan. Testar att starta om"


@app.route("/gendercounter/<string:name>/")
def getGender(name):
    import gendercounter
    namnet = gendercounter.from_string(name)
    return str(namnet.genderfrequency())










if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
