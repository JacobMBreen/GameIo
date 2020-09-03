import os
from flask import Flask, session, render_template

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/uploads'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.before_request
    def before_request_func():
        if not session.get('logged_in'):
            session['logged_in'] = False
            session['user'] = None

    @app.context_processor
    def inject_user():
        user = {
            "logged_in": session['logged_in'],
            "user_data": session['user']
        }
        return dict(user=user)

    @app.after_request
    def after_request_func(response):
        app.logger.info('################SESSIONINFO#######################')
        app.logger.info(session)
        #OPTIONAL - enable to clear flash
        #session.pop('_flashes', None)
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    router(app)
    return app


def router(app):

    from app.controllers import Home
    from app.controllers import Account
    # from app.views import Images

    app.register_blueprint(Home.bp)
    app.register_blueprint(Account.bp)
    # app.register_blueprint(images.bp)