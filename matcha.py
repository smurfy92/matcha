from flask import Flask, session, render_template, redirect, url_for, request, escape
from flaskext.mysql import MySQL
 
mysql = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toto'
app.config['MYSQL_DATABASE_DB'] = 'matcha'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def index():
	if 'username' in session :
		return 'Logged in as %s' % escape(session['username'])
	else:	
		return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form["email"]
		password = request.form["password"]
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
		data = cursor.fetchone()
		if data is None:
			return "Username or Password is wrong"
		else:
			session["username"] = request.form["email"]
			return redirect(url_for("index"))
	else:
		return render_template('login.html')


@app.route("/create", methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		username = request.form["email"]
		password = request.form["password"]
		if len(username) < 5:
			return render_template('create.html', error="email")
		if len(password) < 5:
			return render_template('create.html', error="password")
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
		data = cursor.fetchone()
		if data is None:
			session["username"] = request.form["email"]
			return redirect(url_for("index"))
		else:
			return "invalid email"
	else:
		return render_template('create.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run()
