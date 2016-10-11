from flask import *
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def test_route():
	
	db = connect_to_database()
	cur = db.cursor()

	if 'username' in session:
		inSession = True
		cur.execute('SELECT albumID FROM Album WHERE access=%s OR username=%s UNION \
		SELECT albumID FROM AlbumAccess WHERE username=%s', ('public', session['username'], session['username']))
		results = cur.fetchall()
	else:
		inSession = False
		cur.execute('SELECT albumID FROM Album WHERE access=%s', ['public'])
		results = cur.fetchall()

	cur.execute('SELECT username FROM Album WHERE access=%s', ['public'])
	users = cur.fetchall()
	print inSession
	options = { 
  		"results": results,
  		"inSession": inSession,
  		"users": users
 	}

	return render_template('index.html', **options)