from flask import *
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET', 'POST'])
def test_route():
	
	db = connect_to_database()
	cur = db.cursor()


	firstname = ""
	lastname = ""
	if 'username' in session:
		inSession = True

		cur.execute('SELECT firstname, lastname FROM User WHERE username=%s', [session['username']])
		name = cur.fetchall()
		firstname = name[0]['firstname']
		lastname = name[0]['lastname']

		cur.execute('SELECT albumID FROM Album WHERE access=%s OR username=%s UNION \
		SELECT albumID FROM AlbumAccess WHERE username=%s', ('public', session['username'], session['username']))
		results = cur.fetchall()
	else:
		inSession = False
		cur.execute('SELECT albumID FROM Album WHERE access=%s', ['public'])
		results = cur.fetchall()

	cur.execute('SELECT DISTINCT username FROM Album WHERE access=%s', ['public'])
	users = cur.fetchall()
	options = { 
		"results": results,
		"inSession": inSession,
		"users": users,
		"firstname": firstname,
		"lastname": lastname
 	}

	return render_template('index.html', **options)