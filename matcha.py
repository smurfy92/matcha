from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
@app.route("/coucou")
@app.route("/coucou/<name>")
def coucou(name=None):
	return render_template('coucou.html', name=name)


if __name__ == "__main__":
    app.run()