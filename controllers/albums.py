from flask import *
from extensions import *
from config import *
from os import *

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums/edit', methods = ['GET', 'POST'])
def albums_edit_route():
	firstname = ""
	lastname = ""
	db = connect_to_database()
	cur = db.cursor()
		
	if not 'username' in session:
		return redirect(url_for('log.login_route'))

	#check for username args
	user = session['username']


	if request.method == 'POST':

		if request.form.get('op') == 'delete':
			albumID = request.form.get('albumid')
			cur.execute("SELECT picID from Contain WHERE albumID=%s", [albumID])
			badPics = cur.fetchall()
			for x in badPics:
				picid = x['picID']
				cur.execute("SELECT format from Photo where picID = %s", [picid])
				format = cur.fetchall()
				format = format[0]['format']
				location = "static/images/images/" + picid + "." + format
				remove(path.join(getcwd(), location))
				print location, "deleted"
				cur.execute("DELETE FROM Contain WHERE picID=%s", [picid])
  				cur.execute("DELETE FROM Photo WHERE picID = %s", [picid])
		
			cur.execute("DELETE FROM Album WHERE albumID=%s", [albumID])
			cur.execute("DELETE FROM AlbumAccess WHERE albumID=%s", [albumID])

		
		if request.form.get('op') == 'add':
			user = request.form.get('username')
			newAlbum = request.form.get('title')
			access = 'private'
			cur.execute("INSERT INTO Album (title, username, access) VALUES (%s, %s, %s)", ([newAlbum], [user], access))


	cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [user])
	name = cur.fetchall()
	firstname = name[0]['firstname']
	lastname = name[0]['lastname']

	cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
	albumTitles = cur.fetchall()


	options = {
		"edit": True,
		"albumTitles": albumTitles,
		"user": user,
		"inSession": True,
		"owner": True,
		"firstname": firstname,
		"lastname": lastname
	}
	return render_template("albums.html", **options)


@albums.route('/albums', methods = ['GET','POST'])
def albums_route():

	db = connect_to_database()
	cur = db.cursor()

	firstname = ""
	lastname = ""
	owner = False
	if request.args.get('username'):
		inSession = False
		if 'username' in session:
			inSession = True
		user = request.args.get('username')
		cur.execute("SELECT title, albumID FROM Album WHERE username = %s AND access=%s", ([user], 'public'))
		albumTitles = cur.fetchall()
		if not albumTitles:
			return render_template('404.html'), 404
	else:
		cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
		name = cur.fetchall()
		firstname = name[0]['firstname']
		lastname = name[0]['lastname']
		user = session['username']
		owner = True
		inSession = True
		cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
		albumTitles = cur.fetchall()


	options = {
		"edit": False,
		"albumTitles": albumTitles,
		"user": user,
		"inSession": inSession,
		"owner" : owner,
		"firstname": firstname,
		"lastname": lastname
	}
	return render_template("albums.html", **options)