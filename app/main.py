from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)




temp = '''         <div class="col-md-4">
          <div class="card mb-4 shadow-sm">
            <svg class="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail"><title>Placeholder</title><rect width="100%" height="100%" fill="#55595c"/><text x="50%" y="50%" fill="#eceeef" dy=".3em">Thumbnail</text></svg>
            <div class="card-body">
              <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
              <div class="d-flex justify-content-between align-items-center">
                <div class="btn-group">
                  <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                  <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                </div>
                <small class="text-muted">9 mins</small>
              </div>
            </div>
          </div>
        </div>
        '''






@app.route("/")
def root():
    result = {'Projekt 1':"Naturvetenskap",
              'Projekt 2':"humaniora",
              'Projekt 3':"skola"}
    return render_template("index.html", result = result)

@app.route("/<string:query>/")
def query(query):
    result = {'Projektnamn': query}
    return render_template('index.html', result = result)

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
