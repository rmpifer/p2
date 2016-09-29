from flask import *
from extensions import *
from config import *
from hashlib import md5

album = Blueprint('album', __name__, template_folder='templates')

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():

	albumid = request.args.get('albumid')

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'POST':
		if request.form.get('op') == "add":
			m = md5()
			m.update(str(albumid))
			m.update(str(request.form.get('newFile')))
			values = (sequenceNum, albumID, m.hexdigest(), "")
			cur.execute("INSERT INTO Photo (picID, format) VALUES (%s, jpg", m.hexdigest())
			cur.execute("INSERT INTO Contain (sequenceNum, albumID, picID, caption)\
				VALUES (%s, %s, %s, %s", values)

		if request.form.get('op') == "delete":
			cur.execute("SELECT picID from Contain WHERE picID=%s", [request.form.get('picid')])
			badPic = cur.fetchall()
			cur.execute("DELETE FROM Contain WHERE picID = %s", [badPic['picID']])
			cur.execute("DELETE FROM Photo WHERE picID = %s", [badPic['picID']])

	cur.execute("SELECT picID FROM Contain WHERE albumID = %s", [albumid])
	pics = cur.fetchall()
	cur.execute("SELECT title FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()
	


	options = {
		"edit": True,
		"pics": pics,
		"albumid": albumid,
		"title": title
	}
	return render_template("album.html", **options)

@album.route('/album', methods=['GET','POST'])
def album_route():

	albumid = request.args.get('albumid')

	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT picID FROM Contain WHERE albumID = %s", [albumid])
	pics = cur.fetchall()
	cur.execute("SELECT title FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()

	options = {
		"edit": False,
		"pics": pics,
		"albumid": albumid,
		"title": title
	}
	return render_template("album.html", **options)
