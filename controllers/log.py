from flask import *
from extensions import *


log = Blueprint('log', __name__, template_folder='templates')

@log.route('/login', methods=['GET', 'POST'])
def login_route():
	
	if 'username' in session:
		return redirect(url_for('user.user_edit_route'))

	return render_template("log.html")

'''@log.route('/logout', methods=['GET', 'POST'])
def logout_route():
	if request.method == 'POST':
		session.pop('username', None)
		return redirect(url_for('main.test_route'))'''