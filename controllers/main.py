from flask import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
    return render_template("index.html")


@main.route('/hello')
def hello():
	return "<h1>Hello everyone!</h1>"

