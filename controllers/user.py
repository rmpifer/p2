from flask import *
from extensions import *
import hashlib
import uuid
import re

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():
	firstname = ""
	lastname = ""
	message = []

	db = connect_to_database()
	cur = db.cursor()

	cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
	name = cur.fetchall()
	firstname = name[0]['firstname']
	lastname = name[0]['lastname']

	if request.method == 'POST':
		if request.form.get('firstname'):
			firstname = request.form.get('firstname')
			if len(firstname) > 20:
				message.append("Firstname must be no longer than 20 characters")

			if len(message) == 0:
				cur.execute('UPDATE User SET firstName=%s WHERE username=%s', (firstname, session['username']))

		if request.form.get('lastname'):
			lastname = request.form.get('lastname')
			if len(lastname) > 20:
				message.append("Lastname must be no longer than 20 characters")

			if len(message) == 0:
				cur.execute('UPDATE User SET lastName=%s WHERE username=%s', (lastname, session['username']))

		if request.form.get('email'):
			email = request.form.get('email')
			if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
				message.append("Email address must be valid")
			if len(email) > 40:
				message.append("Email must be no longer than 40 characters")

			if len(message) == 0:
				cur.execute('UPDATE User SET email=%s WHERE username=%s', (email, session['username']))

		if request.form.get('password1'):
			password1 = request.form.get('password1')
			password2 = request.form.get('password2')
			if len(password1) < 8:
				message.append("Passwords must be at least 8 characters long")
			if not re.match("^(?=.*[a-zA-z])(?=.*\d)", password1):
				message.append("Passwords must contain at least one letter and one number")
			if not re.match("^[\w\d_]*$", password1):
				message.append("Passwords may only contain letters, digits, and underscores")
			if password1 != password2:
				message.append("Passwords do not match")

			if len(message) == 0:
				algorithm = 'sha512'
				salt = uuid.uuid4().hex
				m = hashlib.new(algorithm)
				m.update(salt + password1)
				password_hash = m.hexdigest()
		 		password = '$'.join([algorithm, salt, password_hash])
		 		cur.execute('UPDATE User SET password=%s WHERE username=%s', (password, session['username']))

	options = { 
		"edit": True,
		"message": message,
		"inSession": True,
		"firstname": firstname,
		"lastname": lastname
	}

	return render_template('user.html', **options)


@user.route('/user', methods=['GET', 'POST'])
def user_route():

	message = []
	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('user.user_edit_route'))


	if request.method == 'POST':
		username = request.form.get('username')
		if username == "":
			message.append("Username may not be left blank")
		if len(username) > 20:
			message.append("Username must be no longer than 20 characters")
		cur.execute("SELECT username FROM User WHERE username=%s", [username])
		if len(cur.fetchall()) != 0:
			message.append("This username is taken")
		if len(username) < 3:
			message.append("Usernames must be at least 3 characters long")
		if not re.match("^[\w\d_]*$", username):
			message.append("Usernames may only contain letters, digits, and underscores")


		firstname = request.form.get('firstname')
		if firstname == "":
			message.append("Firstname may not be left blank")
		if len(firstname) > 20:
			message.append("Firstname must be no longer than 20 characters")

		lastname = request.form.get('lastname')
		if lastname == "":
			message.append("Lastname may not be left blank")
		if len(lastname) > 20:
			message.append("Lastname must be no longer than 20 characters")

		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		if password1 == "":
			message.append("Password may not be left blank")
		if len(password1) < 8:
			message.append("Passwords must be at least 8 characters long")
		if not re.match("^(?=.*[a-zA-z])(?=.*\d)", password1):
			message.append("Passwords must contain at least one letter and one number")
		if not re.match("^[\w\d_]*$", password1):
			message.append("Passwords may only contain letters, digits, and underscores")
		if password1 != password2:
			message.append("Passwords do not match")

		email = request.form.get('email')
		if email == "":
			message.append("Email may not be left blank")
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			message.append("Email address must be valid")
		if len(email) > 40:
			message.append("Email must be no longer than 40 characters")

		if len(message)==0:
			algorithm = 'sha512'
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hash = m.hexdigest()
	 		password = '$'.join([algorithm, salt, password_hash])

			cur.execute('INSERT INTO User(username, password, firstName, lastName, email)\
				VALUES (%s, %s, %s, %s, %s)', (username, password, firstname, lastname, email))
			return redirect(url_for('log.login_route'))


	options = { 
		"edit": False,
		"message": message,
		"inSession": False,
	}

	return render_template('user.html', **options)