from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session, flash
from flask import current_app as flask_app

class Account():

    def __init__(self):
        """
        Initialise class with configuration 

        """

        self.user = User()
        return None

    def register(self, request):
        """ 
        Registration method. 
    
        Processes POST request, and registers user in Firebase on success

        Parameters: 
            request (obj): The POST request object
    
        Raises: 
            error (Exception): Error from failed Firebase request
    
        """

        # Extract required fields from POST request
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Validates required registration fields
        error = None
        if not email:
            error = 'An email is required.'
        elif not password:
            error = 'Password is required.'
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        elif not password_confirm:
            error = 'Password confirmation is required.'
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                user_data = {
                    "localId": "",
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "avatar": ""
                }
                # Attempt to process valid registration request
                database = Database()
                user_auth = database.register(user_data, password)
            except Exception as err:
                # Raise error from failed Firebase request
                error = err
        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            # Return on success
            return
        
    def login(self, request):
        """

        It gets the users login credentials from the form 
        and then sends it to the database

        """
        # check he have a form post
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            error = None
            if not email:
                # The  user hasn't put in an email
                error = 'An email is required.'
            elif not password:
                # The user hasn't put in a password
                error = 'Password is required.'
            else:
                # Try to log the user in
                try:
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def update(self, request):
        """ 
        It gets the users data from the form 
        and then sends it to the database

        """

        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            if not first_name:
                error = 'A first name is required.'
            elif not last_name:
                error = 'A last name is required.'
            else:
                # If the user has uploaded an image, handle the file upload
                if 'avatar' in request.files:
                    file = request.files['avatar']
                    if file.filename:
                        uploader = Upload()
                        avatar = uploader.upload(file, session['user']['localId'])
                        session['user']['avatar'] = "/" + avatar.strip("/")

                # try to update the user's data
                try:
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                    session.modified = True
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def like(self, image_id, like, request):

        """ 
        It adds a liked image to the users image
        
        """
                
        changed = False
        likes = session['user']['likes']

        if like == 'true':
            if image_id not in likes:
                likes.append(image_id)
                changed = True
        else:
            if image_id in likes:
                likes.remove(image_id)
                changed = True

        if changed:
            session['user']['likes'] = likes
            database = Database()
            database.update_user(session['user'])
            session.modified = True

        return changed
        
    def logout(self):
        self.user.unset_user()

