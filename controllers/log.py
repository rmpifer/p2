from flask import *
from extensions import *
import hashlib
import uuid

log = Blueprint('log', __name__, template_folder='templates')

@log.route('/login', methods=['GET', 'POST'])
def login_route():
	
	message = []
	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'POST':
		username = request.form.get('username')
		if username == "":
			message.append("Username may not be left blank")
		cur.execute("SELECT username FROM User WHERE username=%s", [username])
		user = cur.fetchall()

		password_in = request.form.get('password')
		if password_in == "":
			message.append("Password may not be left blank")

		cur.execute('SELECT password FROM User WHERE username=%s', [username])
		password = cur.fetchall()
		if len(password) == 0:
			message.append("Username does not exist")


		if len(message) == 0:
			password = password[0]['password']
			realPassword = password
			passInfo = password.rsplit('$', 2)
			algorithm = passInfo[0]
			salt = passInfo[1]

			m = hashlib.new(algorithm)
			m.update(salt + password_in)
			password_hash = m.hexdigest()

			if '$'.join([algorithm, salt, password_hash]) == realPassword:
				session['username'] = request.form.get('username')
				return redirect(url_for('main.test_route'))
			else:
				message.append("Password is incorrect for the specified username")

			
	options = {
		"message": message 
	}

	return render_template("log.html", **options)

@log.route('/logout')
def logout_route():
	session.pop('username', None)
	return redirect(url_for('main.test_route'))