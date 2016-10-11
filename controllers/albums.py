from flask import *
from extensions import *
from config import *
from os import *

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums/edit', methods = ['GET', 'POST'])
def albums_edit_route():
	if request.method == 'GET':

		user = session['username']
		db = connect_to_database()
  		cur = db.cursor()

  	if request.method == 'POST':
		user = session['username']
		db = connect_to_database()
		cur = db.cursor()

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
			cur.execute("DELETE FROM AlbumAccess WHERE albumID=%s", albumID)

		
		if request.form.get('op') == 'add':
			user = request.form.get('username')
			newAlbum = request.form.get('title')
			access = 'private'
			cur.execute("INSERT INTO Album (title, username, access) VALUES (%s, %s, %s)", ([newAlbum], [user], access))

	cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
	albumTitles = cur.fetchall()


	options = {
		"edit": True,
		"albumTitles": albumTitles,
		"user": user,
		"inSession": True,
		"owner": True
	}
	return render_template("albums.html", **options)


@albums.route('/albums', methods = ['GET','POST'])
def albums_route():

	owner = False
	if 'username' in session:
		if not request.args.get('username'):
			user = session['username']
			owner = True
		else:
			user = request.args.get('username')
		inSession = True
	else:
		user = request.args.get('username')
		inSession = False

	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
	albumTitles = cur.fetchall()


	options = {
		"edit": False,
		"albumTitles": albumTitles,
		"user": user,
		"inSession": inSession,
		"owner" : owner
	}
	return render_template("albums.html", **options)