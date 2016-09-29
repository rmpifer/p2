from flask import *
from extensions import *
from config import *
from os import *

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums/edit', methods = ['GET', 'POST'])
def albums_edit_route():
	if request.method == 'GET':

		user = request.args.get('username')

		db = connect_to_database()
  		cur = db.cursor()

  	if request.method == 'POST':

  		user = request.args.get('username')
		albumID = request.form.get('albumid')

		db = connect_to_database()
  		cur = db.cursor()

  		if request.form.get('op') == 'delete':
  			cur.execute("SELECT picID from Contain WHERE albumID=%s", [albumID])
  			badPics = cur.fetchall()
	  		for x in badPics:
	  			picid = x['picID']
	  			cur.execute("SELECT format from Photo where picID = %s", [x['picID']])
	  			format = cur.fetchall()
	  			format = format[0]['format']
	  			location = "static/images/images/" + picid + "." + format
	  			remove(path.join(getcwd(), location))
	  			cur.execute("DELETE FROM Contain WHERE picID=%s", [picid])
  				cur.execute("DELETE FROM Photo WHERE picID = %s", [picid])
	  		cur.execute("DELETE FROM Album WHERE albumID=%s", [albumID])
		
	  	if request.form.get('op') == 'add':
	  		newAlbum = request.form.get('title')
	  		insert_statement = "INSERT INTO Album (title, username) VALUES (%s, %s)"
	  		arguments = ([newAlbum], [user])
	  		cur.execute(insert_statement, arguments)

  	cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
  	albumTitles = cur.fetchall()


	options = {
		"edit": True,
		"albumTitles": albumTitles,
		"user": user
	}
	return render_template("albums.html", **options)


@albums.route('/albums', methods = ['GET','POST'])
def albums_route():
	if request.method == 'GET':

		user = request.args.get('username')

		db = connect_to_database()
  		cur = db.cursor()
  		cur.execute("SELECT title, albumID FROM Album WHERE username = %s", [user])
  		albumTitles = cur.fetchall()

	options = {
		"edit": False,
		"albumTitles": albumTitles,
		"user": user
	}
	return render_template("albums.html", **options)