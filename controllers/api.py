from flask import *
from extensions import *
from os import *
import hashlib
import uuid
import re


api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/v1/user', methods=['GET', 'POST', 'PUT'])
def user_api_route():

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'GET':
		if 'username' in session:
			username = session['username']
			cur.execute('SELECT firstName, lastName, email FROM User WHERE username=%s', username)
			userInfo = cur.fetchall();
			firstname = userInfo['firstName']
			lastname = userInfo['lastName']
			email = userInfo['email']
			userDict = {
				"username": username,
				"firstname": firstname,
				"lastname": lastname,
				"email": email
			}

			return jsonify(userDict)
		else:
			return jsonify({
					"errors": {"message": "You do not have the necessary credentials for the resource"}
				}), 401

	elif request.method == 'POST':
		newUser = request.get_json();

		if 'username' not in newUser or 'firstname' not in newUser or 'lastname' not in newUser or 'password1' not in newUser or 'password2' not in newUser or 'email' not in newUser:
			return jsonify({
				"errors": {"message": "You did not provide the necessary fields"}
				}), 422

		username = newUser['username']
		firstname = newUser['firstname']
		lastname = newUser['lastname']
		password1 = newUser['password1']
		password2 = newUser['password2']
		email = newUser['email']

		message = []
		#Check is a valid Username
		cur.execute("SELECT username FROM User WHERE username=%s", username)
		if len(cur.fetchall()) != 0:
			message.append({"message": "This username is taken"})
		if len(username) < 3:
			message.append({"message": "Usernames must be at least 3 characters long"})
		if not re.match("^[\w\d_]*$", username):
			message.append({"message": "Usernames may only contain letters, digits, and underscores"})

		#Check is a valid Password
		if len(password1) < 8:
			message.append({"message": "Passwords must be at least 8 characters long"})
		if not re.match("^(?=.*[a-zA-z])(?=.*\d)", password1):
			message.append({"message": "Passwords must contain at least one letter and one number"})
		if not re.match("^[\w\d_]*$", password1):
			message.append({"message": "Passwords may only contain letters, digits, and underscores"})
		if password1 != password2:
			message.append({"message": "Passwords do not match"})

		#Check is a valid Email
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			message.append({"message": "Email address must be valid"})	
			

		if len(username) > 20:
			message.append({"message": "Username must be no longer than 20 characters"})	
		if len(firstname) > 20:
			message.append({"message": "Firstname must be no longer than 20 characters"})	
		if len(lastname) > 20:
			message.append({"message": "Lastname must be no longer than 20 characters"})		
		if len(email) > 40:
			message.append({"message": "Email must be no longer than 40 characters"})


		if len(message)==0:
			algorithm = 'sha512'
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hash = m.hexdigest()
	 		password = '$'.join([algorithm, salt, password_hash])

			cur.execute('INSERT INTO User(username, password, firstName, lastName, email)\
				VALUES (%s, %s, %s, %s, %s)', (username, password, firstname, lastname, email))

			userDict = {
				"username": username,
				"firstname": firstname,
				"lastname": lastname,
				"email": email
			}

			return jsonify(userDict), 201
		else:
			return jsonify({
					"errors": message
				}), 422

	elif request.method == 'PUT':
		updateUser = request.get_json()

		username = session['username']
		checkUsername = updateUser['username']

		if username == checkUsername:

			firstname = updateUser['firstname']
			lastname = updateUser['lastname']
			password1 = updateUser['password1']
			password2 = updateUser['password2']
			email = updateUser['email']


			#Check is a valid Password
			if len(password1) < 8:
				message.append({"message": "Passwords must be at least 8 characters long"})
			if not re.match("^(?=.*[a-zA-z])(?=.*\d)", password1):
				message.append({"message": "Passwords must contain at least one letter and one number"})
			if not re.match("^[\w\d_]*$", password1):
				message.append({"message": "Passwords may only contain letters, digits, and underscores"})
			if password1 != password2:
				message.append({"message": "Passwords do not match"})

			#Check is a valid Email
			if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
				message.append({"message": "Email address must be valid"})	
				

			if len(firstname) > 20:
				message.append({"message": "Firstname must be no longer than 20 characters"})	
			if len(lastname) > 20:
				message.append({"message": "Lastname must be no longer than 20 characters"})		
			if len(email) > 40:
				message.append({"message": "Email must be no longer than 40 characters"})


			if len(message)==0:
				algorithm = 'sha512'
				salt = uuid.uuid4().hex
				m = hashlib.new(algorithm)
				m.update(salt + password1)
				password_hash = m.hexdigest()
		 		password = '$'.join([algorithm, salt, password_hash])

				cur.execute('INSERT INTO User(username, password, firstName, lastName, email)\
					VALUES (%s, %s, %s, %s, %s)', (username, password, firstname, lastname, email))

				userDict = {
					"username": username,
					"firstname": firstname,
					"lastname": lastname,
					"email": email
				}

				return jsonify(userDict), 201
			else:
				return jsonify({
						"errors": message
					}), 422

		else:
			jsonify({
				"errors": {"message": "You do not have the necessary permissions for the resource"}
			}), 403


@api.route('/api/v1/login', methods=['POST'])
def login_api_route():

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'POST':
		checkUser = request.get_json()

		if 'username' not in checkUser or 'password' not in checkUser:
			print "could not find"
			return jsonify({
					"errors": {"message": "You did not provide the necessary fields"}
				}), 422
		username = checkUser['username']
		inPassword = checkUser['password']


		cur.execute('SELECT password FROM User WHERE username=%s', [username])
		password = cur.fetchall()
		if len(password) == 0:
			return jsonify({
				"errors": {"message": "Username does not exist"}
			}), 404


		password = password[0]['password']
		realPassword = password
		passInfo = password.rsplit('$', 2)
		algorithm = passInfo[0]
		salt = passInfo[1]

		m = hashlib.new(algorithm)
		m.update(salt + inPassword)
		password_hash = m.hexdigest()

		if '$'.join([algorithm, salt, password_hash]) == realPassword:
			session['username'] = username

			validUser = {
				"username": username
			}
			return jsonify(validUser)
		else:
			return jsonify({
				"errors": {"message": "Password is incorrect for the specified username"}
			}), 422


@api.route('/api/v1/logout', methods=['POST'])
def logout_api_route():

	if request.method == 'POST':
		if 'username' in session:
			session.pop('username', None)
			return jsonify(), 204
		else:
			return jsonify({
				"errors": {"message": "You do not have the necessary credentials for the resource"}
				}), 401


@api.route('/api/v1/album/<albumid>', methods=['GET'])
def album_api_route(albumid):

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'GET':

		print "test"
		cur.execute("SELECT title, access FROM Album WHERE albumID = %s", albumid)
		title = cur.fetchall()
		print "server1"
		if not title:
			return jsonify({
				"errors": {"message": "The requested resource could not be found"}
				}), 404


		if title[0]['access'] == 'private':
			if 'username' in session:

				cur.execute("SELECT * FROM Album WHERE albumID=%s and username=%s", (albumid, session['username']))
				owner = cur.fetchall()
				print "server2"

				if len(owner) == 0:
					cur.execute("SELECT * FROM AlbumAccess WHERE username=%s AND albumID=%s", (session['username'], albumid))
					permission = cur.fetchall()
					print "server3"

					if len(permission) == 0:
						return jsonify({
							"errors": {"message": "You do not have the necessary permissions for the resource"}
						}), 403
			else:
				return jsonify({
					"errors": {"message": "You do not have the necessary credentials for the resource"}
					}), 401

		cur.execute('SELECT access, created, lastUpdate, title, username FROM Album WHERE albumID=%s', albumid)
		albumInfo = cur.fetchall()

		access = albumInfo[0]['access']
		created = albumInfo[0]['created']
		lastupdated = albumInfo[0]['lastUpdate']
		title = albumInfo[0]['title']
		username = albumInfo[0]['username']

		cur.execute('SELECT * FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID=%s', albumid)
		pics = cur.fetchall()

		album = {
			"access": access,
			"albumid": albumid,
			"created": created,
			"lastupdated": lastupdated,
			"pics": pics,
			"title": title,
			"username": username
		}

		return jsonify(album)


@api.route('/api/v1/pic/<picid>', methods=['GET'])
def pic_api_route(picid):

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'GET':

		cur.execute("SELECT albumID FROM Contain WHERE picID = %s", [picid])
		albumid = cur.fetchall()
		if not albumid:
			return jsonify({
				"errors": {"message": "The requested resource could not be found"}
				}), 404

		albumid = albumid[0]['albumID']

		cur.execute("SELECT access FROM Album WHERE albumID=%s", [albumid])
		access = cur.fetchall()

		if access[0]['access'] == 'private':
			if 'username' in session:
				cur.execute("SELECT username FROM Album WHERE albumID=%s and username=%s", ([albumid], session['username']))
				owner = cur.fetchall()
				if len(owner) == 0:
					cur.execute("SELECT username FROM AlbumAccess WHERE username=%s AND albumID=%s", (session['username'], albumid))
					permission = cur.fetchall()
					if len(permission) == 0:
						return jsonify({
							"errors": {"message": "You do not have the necessary permissions for the resource"}
						}), 403
			else:
				return jsonify({
					"errors": {"message": "You do not have the necessary credentials for the resource"}
					}), 401

		owner = False
		if 'username' in session:
			inSession = True

			cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
			name = cur.fetchall()
			firstname = name[0]['firstname']
			lastname = name[0]['lastname']
			
			cur.execute("SELECT username FROM Album WHERE albumID=%s and username=%s", ([albumid], session['username']))
			owner = cur.fetchall()
			if len(owner) != 0:
				owner = True


		cur.execute("SELECT picID FROM Contain WHERE albumID = %s ORDER BY sequenceNum", [albumid])
		picList = cur.fetchall()
		counter = 0
		for pic in picList:
			if pic['picID'] == picid:
				break
			counter += 1

		previd = counter - 1
		nextid = counter + 1
		isFirst = False
		isLast = False
		if counter == 0:
			isFirst = True
		if counter == len(picList)-1:
			isLast = True

		if not isFirst:
			previd = picList[previd]['picID']
		if not isLast:
			nextid = picList[nextid]['picID']


		cur.execute("SELECT Photo.format, Contain.caption FROM Photo JOIN Contain WHERE Contain.picID=Photo.picID AND Contain.picID=%s", [picid])
		pic = cur.fetchall()
		format = pic[0]['format']
		caption = pic[0]['caption']

	elif request.method == 'PUT':
		pic = request.get_json()

		if 'albumid' not in pic or 'caption' not in pic or 'format' not in pic or 'next' not in pic or 'picid' not in pic or 'prev' not in picid:
			return jsonify({
				"errors": {"message": "You did not provide the necessary fields"}
				}), 422
		albumid = pic['albumid']
		caption = pic['caption']
		format = pic['format']
		next = pic['next']
		picid = pic['picid']

		cur.execute('SELECT * FROM Photo WHERE picID=%s', [picid])
		if not cur.fetchall():
			return jsonify({
				"errors": {"message": "The requested resource could not be found"}
				}), 404
		prev = pic['prev']

		cur.execute('UPDATE Contain SET caption=%s WHERE picid=%s', (caption, picid))
		cur.execute('UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s', albumid)

	print format
	picInfo = {
		"albumid": albumid,
		"caption": caption,
		"format": format,
		"next": nextid,
		"picid": picid,
		"prev": previd
	}

	return jsonify(picInfo)

