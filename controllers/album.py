from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


album = Blueprint('album', __name__, template_folder='templates')


UPLOAD_FOLDER = 'static/images/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	firstname = ""
	lastname = ""
	db = connect_to_database()
	cur = db.cursor()
	if not 'username' in session:
		abort(403)

	private = False
	if request.method == 'GET':
		albumid = request.args.get('albumid')


	if request.method == 'POST':
		albumid = request.form.get('albumid')
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
			picid = request.form.get('picid')
			cur.execute("SELECT format FROM Photo WHERE picID=%s", [picid])
			badPic = cur.fetchall()
			format = badPic[0]['format']
			location = "static/images/images/" + picid + "." + format
			remove(path.join(getcwd(), location))
			cur.execute("DELETE FROM Contain WHERE picID=%s", [picid])
			cur.execute("DELETE FROM Photo WHERE picID = %s", [picid])
			cur.execute("UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s", albumid)

		if request.form.get('op') == 'grant':
			username = request.form.get('username')
			cur.execute('INSERT INTO AlbumAccess(albumID, username) VALUES (%s, %s)', (albumid, username))

		if request.form.get('op') == 'revoke':
			username = request.form.get('username')
			cur.execute('DELETE FROM AlbumAccess WHERE username=%s AND albumID=%s', (username, albumid))

		if request.form.get('op') == 'access':
			access = request.form.get('access')
			cur.execute("UPDATE Album SET access=%s WHERE albumID=%s", (access, albumid))
			cur.execute("UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s", [albumid])
			if access == 'public':
				cur.execute("DELETE FROM AlbumAccess WHERE albumID=%s", [albumid])
			if access == 'private':
				private = True

	
	cur.execute('SELECT username FROM AlbumAccess WHERE albumID=%s', [albumid])
	access = cur.fetchall()
	cur.execute("SELECT title FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()
	cur.execute("SELECT Contain.picID, Photo.format FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
	pics = cur.fetchall()
	cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
	name = cur.fetchall()
	firstname = name[0]['firstname']
	lastname = name[0]['lastname']
	cur.execute("SELECT username FROM Album WHERE albumID=%s", [albumid])
	owner = cur.fetchall()
	cur.execute("SELECT firstname, lastname FROM User WHERE username=%s", [owner[0]['username']])	
	owner = cur.fetchall()
	owner = owner[0]['firstname'] + " " + owner[0]['lastname']

	options = {
		"edit": True,
		"pics": pics,
		"albumid": albumid,
		"title": title,
		"access": access,
		"inSession": True,
		"firstname": firstname,
		"lastname": lastname,
		"private": private,
		"owner": owner
	}
	return render_template("album.html", **options)

@album.route('/album', methods=['GET','POST'])
def album_route():
	firstname = ""
	lastname = ""
	albumid = request.args.get('albumid')

	db = connect_to_database()
	cur = db.cursor()

	cur.execute("SELECT title, access FROM Album WHERE albumID = %s", [albumid])
	title = cur.fetchall()

	inSession = False
	if title[0]['access'] == 'private':
		if 'username' in session:

			cur.execute("SELECT username FROM Album WHERE albumID=%s and username=%s", ([albumid], session['username']))
			owner = cur.fetchall()
			if len(owner) == 0:
				cur.execute("SELECT username FROM AlbumAccess WHERE username=%s AND albumID=%s", (session['username'], albumid))
				permission = cur.fetchall()
				if len(permission) == 0:
					abort(403)
		else:
			return redirect(url_for('log.login_route'))

	if 'username' in session:
		inSession = True

		cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
		name = cur.fetchall()
		firstname = name[0]['firstname']
		lastname = name[0]['lastname']
			
			
	cur.execute("SELECT username FROM Album WHERE albumID=%s", [albumid])
	owner = cur.fetchall()
	cur.execute("SELECT firstname, lastname FROM User WHERE username=%s", [owner[0]['username']])	
	owner = cur.fetchall()
	owner = owner[0]['firstname'] + " " + owner[0]['lastname']

	cur.execute("SELECT Contain.picID, Photo.format, Photo.posted, Contain.caption FROM Contain JOIN Photo WHERE Contain.picid = Photo.picid AND Contain.albumID = %s", [albumid])
	pics = cur.fetchall()

	options = {
		"edit": False,
		"pics": pics,
		"albumid": albumid,
		"title": title,
		"inSession": inSession,
		"firstname": firstname,
		"lastname": lastname,
		"owner": owner
	}
	return render_template("album.html", **options)
