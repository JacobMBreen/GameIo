from flask import session

class User():

    def __init__(self):
        self.user = None
        self.get_user()

    def is_logged_in(self):
        self.get_user()
        return (self.user != None)
    
    def get_user(self):
        self.user = session.get('user')
        return self.user
    
    def get_user_id(self):
        if (self.is_logged_in()):
            return self.user['localId']
        return False
    
    def get_user_id_token(self):
        if (self.is_logged_in()):
            return self.user['idToken']
        return False

    def set_user(self, user):
        session['logged_in'] = True
        session['user'] = user
        session['user']['likes'] = user.get('likes', [])
        self.get_user()

    def unset_user(self):
        self.user = None
        session['logged_in'] = False
        session['user'] = None
        session.clear()