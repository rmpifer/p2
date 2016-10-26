from flask import *
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET', 'POST'])
def test_route():
	
	db = connect_to_database()
	cur = db.cursor()

	results = []
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

	albums = []
	for result in results:
		cur.execute('SELECT title, albumID FROM Album WHERE albumID=%s', [result['albumID']])
		albumTitle = cur.fetchall()
		albumTitle = albumTitle[0]['title']
		albums.append({"title": albumTitle, "albumid": result['albumID']})

	cur.execute('SELECT DISTINCT username FROM Album WHERE access=%s', ['public'])
	users = cur.fetchall()

	options = { 
		"albums": albums,
		"inSession": inSession,
		"users": users,
		"firstname": firstname,
		"lastname": lastname
 	}

	return render_template('index.html', **options)