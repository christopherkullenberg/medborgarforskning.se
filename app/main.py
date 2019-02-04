from flask import Flask, flash, redirect, render_template, request, session, abort
from bs4 import BeautifulSoup
import requests
import lxml
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World from Flaskan. Testar att starta om"

@app.route("/hello/<string:name>/")
def helloName(name):
    return render_template('namn.html', name=name)

@app.route("/gendercounter/<string:name>/")
def getGender(name):
    import gendercounter
    namnet = gendercounter.from_string(name)
    return str(namnet.genderfrequency())

@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)

@app.route("/flashbackscraper")
def fbscraper():
    r = requests.get("https://telecomix.org/")
    html = r.content
    #soup = BeautifulSoup(html, "lxml")
    return html




if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
