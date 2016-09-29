from flask import *
from extensions import *
from config import *

main = Blueprint('main', __name__, template_folder='templates', url_prefix=env['prefix'])

@main.route('/')
def test_route():


  db = connect_to_database()
  cur = db.cursor()
  cur.execute('SELECT username FROM User')
  results = cur.fetchall()


  options = { 
  		"results": results
  }

  return render_template('index.html', **options)