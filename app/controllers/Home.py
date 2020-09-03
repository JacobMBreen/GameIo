from app.classes.Database import Database
from flask import Blueprint, render_template, flash

bp = Blueprint('home', __name__, url_prefix='', static_folder='../static')

# Load the index page
@bp.route('/')
def index():
    return render_template('home.html')

@bp.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404