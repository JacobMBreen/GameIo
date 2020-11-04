from app.models.Image import Image
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from flask import current_app as flask_app

bp = Blueprint('images', __name__, url_prefix='/images', static_folder='../static')
   
@bp.route('/', methods=['GET', 'POST'])
def images():

    error = None
    images = []
    try:
        image_model = Image()
        images = image_model.get_images()
    except Exception as err:
        error = err
    if error:
        flash(str(error))

    return render_template('images/images.html', images=images, title="All Images")
   
@bp.route('/my-images', methods=['GET', 'POST'])
def my_images():

    error = None
    images = []
    try:
        image_model = Image()
        images = image_model.get_user_images()
    except Exception as err:
        error = err
    if error:
        flash(str(error))

    return render_template('images/my-images.html', images=images, title="My Images")
   
@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    
    if request.method == 'POST':
        error = None
        try:
            image_model = Image()
            image_id = image_model.upload(request)
            flash("This image has been uploaded")
            return redirect(url_for('images.edit', image_id=image_id))
        except Exception as err:
            error = err
        if error:
            flash(str(error))

    return render_template('images/upload.html')
   
@bp.route('/category/<category>', methods=['GET'])
def category(category):

    error = None
    images = []
    category_name = category.replace('-', ' ').title()
    title = category_name + " Images"
    try:
        image_model = Image()
        images = image_model.get_category_images(category)
    except Exception as err:
        error = err
    if error:
        flash(str(error))

    return render_template('images/images.html', images=images, title=title)
    
   
@bp.route('/edit/<image_id>', methods=['GET', 'POST'])
def edit(image_id):

    error = None
    image = []

    if request.method == 'POST':
        try:
            image_model = Image()
            image = image_model.update(image_id, request)
            flash("This image has been updated")
        except Exception as err:
            error = err
    try:
        image_model = Image()
        image = image_model.get_image(image_id)
    except Exception as err:
        error = err
    if error:
        flash(str(error))

    return render_template('images/edit.html', image=image)

@bp.route('/delete/<image_id>', methods=['GET'])
def delete(image_id):
        
    error = None
    image = []
    try:
        image_model = Image()
        image = image_model.delete_image(image_id)
    except Exception as err:
        error = err
    if error:
        flash(str(error))
    else:
        flash('This image has been deleted')

    return redirect(url_for('images.my_images'))
