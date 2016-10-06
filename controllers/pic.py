from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic')
def pic_route():


	db = connect_to_database()
	cur = db.cursor()


	picid = request.args.get('picid')


	cur.execute("SELECT albumID FROM Contain WHERE picID = %s", [picid])
	albumid = cur.fetchall()

	if not albumid:
		response = jsonify({'message': "Bad picid"})
  		response.status_code = 404
  		response.status = 'error.Bad Request'
  		return response

	albumid = albumid[0]['albumID']
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


	cur.execute("SELECT format FROM Photo WHERE picID=%s", [picid])
	format = cur.fetchall()
	format = format[0]['format']


	options = {
		"picid": picid,
		"albumid": albumid,
		"format": format,
		"previd": previd,
		"nextid": nextid,
		"isFirst": isFirst,
		"isLast" : isLast
	}
	return render_template("pic.html", **options)