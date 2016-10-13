from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET', 'POST'])
def pic_route():

	firstname = ""
	lastname = ""
	db = connect_to_database()
	cur = db.cursor()

	if request.method == 'GET':
		picid = request.args.get('picid')

	if request.method == 'POST':
		if request.form.get('op') == 'caption':
			picid = request.form.get('picid')
			caption = request.form.get('caption')
			cur.execute('UPDATE Contain SET caption=%s WHERE picid=%s', (caption, picid))
			cur.execute('SELECT albumID FROM Contain WHERE picID=%s', [picid])
			albumid = cur.fetchall()
			albumid = albumid[0]['albumID']
			cur.execute('UPDATE Album SET lastUpdate=CURRENT_TIMESTAMP() WHERE albumID=%s', [albumid])



	cur.execute("SELECT albumID FROM Contain WHERE picID = %s", [picid])
	albumid = cur.fetchall()
	albumid = albumid[0]['albumID']

	cur.execute("SELECT access FROM Album WHERE albumID=%s", [albumid])
	access = cur.fetchall()

	inSession = False
	if access[0]['access'] == 'private':
		if 'username' in session:
			inSession = True
			cur.execute("SELECT username FROM Album WHERE albumID=%s and username=%s", ([albumid], session['username']))
			owner = cur.fetchall()
			if len(owner) == 0:
				cur.execute("SELECT username FROM AlbumAccess WHERE username=%s AND albumID=%s", (session['username'], albumid))
				permission = cur.fetchall()
				if len(permission) == 0:
					return render_template('403.html'), 403
		else:
			return redirect(url_for('log.login_route'))

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
	format = cur.fetchall()
	format = format[0]


	options = {
		"picid": picid,
		"albumid": albumid,
		"format": format,
		"previd": previd,
		"nextid": nextid,
		"isFirst": isFirst,
		"isLast" : isLast,
		"owner": owner,
		"inSession": inSession,
		"firstname": firstname,
		"lastname": lastname
	}
	return render_template("pic.html", **options)