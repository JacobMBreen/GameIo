import os
import tempfile
import pyrebase
import requests
import json
from collections import OrderedDict
from flask import current_app as flask_app
from app import SITE_ROOT

class Database():
    """ 
    Database Class. 
  
    Class to interact with Firebase Realtime Database. 
  
    """

    def __init__(self):
        """ 
        Initialise class with configuration 
    
        """
        # Load Firebase config data, including Service Account file
        firebase_config_file = os.path.join(SITE_ROOT, 'firebase.json')
        firebase_config = json.load(open(firebase_config_file))
        firebase_config["serviceAccount"] = os.path.join(SITE_ROOT, 'firebase.admin.json')
        
        # Initialize Firebase auth and database
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        # Create readable errors based on Firebase errors
        self.readable_errors = {
            "INVALID_PASSWORD": "This is an invalid password",
            "EMAIL_NOT_FOUND": "This email has not been registered",
            "EMAIL_EXISTS": "This email already exists. Try logging in instead.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts, please try again later",
            "USER_DISABLED": "This account has been disabled by an administrator.",
        }

    def get_images(self, limit=20, user_id=False):
        """
        Method to get 20 latest images
        """
        
        try:
            # Get the user's images
            if (user_id):
                images = self.db.child("images").order_by_child("user_id").equal_to(user_id).limit_to_first(limit).get()
            # gets everyone's images
            else:
                images = self.db.child("images").order_by_child("created_at").limit_to_first(limit).get()

            flask_app.logger.info('####################### images val #####################')
            flask_app.logger.info(images.val())
            # checks if we have the images
            if isinstance(images.val(), OrderedDict):
                return images
            else:
                return False
            
        except Exception as err:
            self.process_error(err)

    def get_category_images(self, category, limit=20):

        """
        Gets images by the category
        """
        # tries to images the category
        try:
            images = self.db.child("images").order_by_child("category").equal_to(category).limit_to_first(limit).get()

            if isinstance(images.val(), OrderedDict):
                return images
            else:
                return False
            
        except Exception as err:
            self.process_error(err)
        
    def get_image(self, image_id):
        """
        gets an image by the id

        """
        
        error = None
        image = False
        
        try:
            image = self.db.child("images").child(image_id).get()

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            return image.val()

    def save_image(self, image_data, image_id):
        """
        saves the images data

        """

        try:
            self.db.child("images").child(image_id).set(image_data)
        except Exception as err:
            self.process_error(err)

    def delete_image(self, image_id):
        """
        delets the whole image based on the id that gets passed in

        """
        try:
            self.db.child("images").child(image_id).remove()
        except Exception as err:
            self.process_error(err)

    def remove_matching_value(self, data, value):
        return_data = []
        for key in data:
            if key != value:
                return_data.append(key)
        return return_data


    # User and Account Requests
    def register(self, user_data, password):
        """ 
        register's the data

        """
        try:
            user_auth = self.auth.create_user_with_email_and_password(user_data['email'], password)
            user_data['localId'] = user_auth['localId']
            self.db.child("users").child(user_auth['localId']).set(user_data)
            return user_auth
        except Exception as err:
            self.process_error(err)

    def login(self, email, password):
        """
        checks the user's credential's for the password and the email.

        """
        try:
            user_auth = self.auth.sign_in_with_email_and_password(email, password)
            user = self.db.child("users").child(user_auth['localId']).get().val()
            return user
        except Exception as err:
            self.process_error(err)

    def update_user(self, user_data):
        """
        updates the users data 
        """ 
        try:
            self.db.child("users").child(user_data['localId']).update(user_data)
            return
        except Exception as err:
            self.process_error(err)
 
    def process_error(self, error):
        flask_app.logger.info(error)
        readable_error = self.get_readable_error(error)
        raise Exception(readable_error)

    def get_readable_error(self, error):
        error_json = error.args[1]
        error_messsage = json.loads(error_json)['error']['message']
        if error_messsage in self.readable_errors.keys(): 
            return self.readable_errors[error_messsage]
        else: 
            return "There was a problem with your request."