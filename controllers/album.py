from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


album = Blueprint('album', __name__, template_folder='templates')


UPLOAD_FOLDER = 'static/images/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():


	albumid = request.args.get('albumid')

	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'POST':
		print "after post"
		if request.form.get('op') == 'add':
			if 'file' not in request.files:
				flash('No file part')
				return redirect(request.url)

			file = request.files['file']

			if file.filename == '':
				flash('No selected file')
				return redirect(request.url)

			if file and allowed_file(file.filename):
				m = md5()
				m.update(str(albumid))
				m.update(file.filename)
				filename = m.hexdigest() + filename.rsplit('.', 1)[1]
				file.save(path.join(config['UPLOAD_FOLDER'], filename))
				cur.execute("SELECT MAX(sequenceNum) FROM Contain")
				sequenceNum = int(cur.fetchall()) + 1
				filename = (m.hexdigest(), filename.rsplit('.', 1)[1])
				values = (sequenceNum, albumID, filename, "")
				cur.execute("INSERT INTO Photo (picID, format) VALUES (%s, %s)", filename)
				cur.execute("INSERT INTO Contain (sequenceNum, albumID, picID, caption) VALUES (%s, %s, %s, %s)", values)

		print "before delete"
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
			

	cur.execute("SELECT Contain.picID, Photo.format FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
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
	cur.execute("SELECT Contain.picID, Photo.format FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
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
