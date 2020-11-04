from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify
from flask import current_app as flask_app
from app.models.Account import Account

bp = Blueprint('account', __name__, url_prefix='', static_folder='../static')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ 
    Registration controller. 
  
    Presents the registration view and handles registration requests. 
  
    Returns: 
    obj: Either render_template or redirect
  
    """

    if request.method == 'POST':
        error = None
        try:
            # Get account singleton and try register user
            account = Account()
            user = account.register(request)
        except Exception as err:
            # Registration error to be flashed
            error = err
        if error:
            flash(str(error))
        else:
            # Registration successful so redirect
            flash("Please login to get started!")
            return redirect(url_for('account.login'))

    return render_template('account/register.html')
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        error = None
        try:
            account = Account()
            user = account.login(request)
        except Exception as err:
            error = err
        if error:
            flash(str(error))
        else:
            flash("Welcome back!")
            return redirect(url_for('account.profile'))

    return render_template('account/login.html')
    
@bp.route('/profile', methods=['GET', 'POST'])
def profile():

    if request.method == 'POST':
        error = None
        try:
            account = Account()
            user = account.update(request)
            flash("Your details have been updated")
        except Exception as err:
            error = err
        if error:
            flash(str(error))

    return render_template('account/profile.html')
    
@bp.route('/logout')
def logout():
    account = Account()
    account.logout()
    return redirect(url_for('home.index'))

@bp.route('/like', methods=['GET'])
def like():

    image_id = request.args.get('image_id')
    like = request.args.get('like')
    flask_app.logger.info('## LIKE VAL CT ##')
    flask_app.logger.info(request.args.get('like'))
    flask_app.logger.info(like)
    response = ''

    try:
        account = Account()
        response = account.like(image_id, like, request)
    except Exception as err:
        response = str(err)
    
    return jsonify(response)
