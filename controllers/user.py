from flask import *
from extensions import *
import hashlib
import uuid
import re

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():

	if 'username' not in session:
		return redirect(url_for('log.login_route'))
	else:
		return render_template('user.html')


@user.route('/user', methods=['GET', 'POST'])
def user_route():

	if 'username' in session:

		return redirect(url_for('user.user_edit_route'))

	return render_template('user.html')