import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app as flask_app
from app import SITE_ROOT

class Upload():

    def __init__(self):
        """
        Instantiates the class

        """"

        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}

    def upload(self, file, filename):
        """
        uploads filename

        """
        allowed_extension = self.allowed_file(file.filename)
        if allowed_extension:
            fullname = filename + '.' + allowed_extension
            destination = os.path.join('static/uploads', fullname)
            file.save(os.path.join(SITE_ROOT, destination))
            return destination
        else:
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    def allowed_file(self, filename):
        """
        it allows the file to be used

        """
        if ('.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions):
            return filename.rsplit('.', 1)[1].lower()
        return False