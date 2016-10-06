from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


album = Blueprint('album', __name__, template_folder='templates')


UPLOAD_FOLDER = 'static/images/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():

	db = connect_to_database()
	cur = db.cursor()

	albumid = request.args.get('albumid')

	cur.execute("SELECT title FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()
	if len(title) == 0:
		abort(404)

	if request.method == 'POST':
		if request.form.get('op') == 'add':
			file = request.files['file']

			if file.filename == '':
				flash('No selected file')
				return redirect(request.url)


			if file and allowed_file(file.filename):

				m = md5()
				m.update(str(albumid))
				m.update(file.filename)
				picid = m.hexdigest()
				format = file.filename.rsplit('.', 1)[1]
				filename = picid + "." + format 

				file.save(path.join(UPLOAD_FOLDER, filename))
				cur.execute("SELECT MAX(sequenceNum) FROM Contain")
				sequenceNum = cur.fetchall()
				sequenceNum = sequenceNum[0]['MAX(sequenceNum)']
				sequenceNum += 1
				cur.execute("INSERT INTO Photo (picID, format) VALUES (%s, %s)", (picid, format ))
				cur.execute("INSERT INTO Contain (sequenceNum, albumID, picID, caption) VALUES (%s, %s, %s, %s)", (sequenceNum, albumid, picid, ""))
				cur.execute("UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s", albumid)

		if request.form.get('op') == 'delete':
			print "after delete"
			picid = request.form.get('picid')
			cur.execute("SELECT format FROM Photo WHERE picID=%s", [picid])
			badPic = cur.fetchall()
			format = badPic[0]['format']
			location = "static/images/images/" + picid + "." + format
			remove(path.join(getcwd(), location))
			cur.execute("DELETE FROM Contain WHERE picID=%s", [picid])
			cur.execute("DELETE FROM Photo WHERE picID = %s", [picid])
			cur.execute("UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s", albumid)
			

	cur.execute("SELECT Contain.picID, Photo.format FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
	pics = cur.fetchall()
	


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

	cur.execute("SELECT title FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()

	if len(title) == 0:
		abort(404)

	cur.execute("SELECT Contain.picID, Photo.format FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
	pics = cur.fetchall()

	options = {
		"edit": False,
		"pics": pics,
		"albumid": albumid,
		"title": title
	}
	return render_template("album.html", **options)
