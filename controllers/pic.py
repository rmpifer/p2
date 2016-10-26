from flask import *
from extensions import *
from config import *
from hashlib import md5
from os import *


pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET', 'POST'])
def pic_route():

	return render_template("single_page.html")