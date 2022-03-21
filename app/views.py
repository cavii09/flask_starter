"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, redirect, url_for, flash, send_from_directory, session 
from app.forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename
import os
import psycopg2


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=['GET', 'POST'])
def new_properties():
    form = PropertyForm()

    if request.method == "POST":
        if form.validate_on_submit():
            property_title=form.property_title.data
            description=form.description.data
            bedrooms = form.bedrooms.data
            bathrooms = form.bathrooms.data
            price = form.price.data
            property_type = form.property_type.data
            location = form.location.data
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            myproperty = Property(property_title,description, bedrooms, bathrooms, price, property_type, location, filename)
            db.session.add(myproperty)
            db.session.commit()
            flash('New Property Added Successfull!', 'success')
        else:
            flash_errors(form)
        return render_template('property.html', form=form)        

def connect_db():
    return psycopg2.connect(host="localhost", database="project1", user="project1.", password="pwproject1")
    
@app.route('/properties/')
def list_properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<propertyid>')
def specific_property(property_id):
    property_id = int(property_id)
    my_property = Property.query.filter_by(id=property_id).first()

    return render_template('individual_property.html', property=my_property)

###
# The functions below should be applicable to all Flask apps.
###
@app.route('/uploads/<filename>')
def get_uploaded_images(filename):
    rootdir = os.getcwd()
    return send_from_directory(os.path.join(rootdir, app.config['UPLOAD_FOLDER']),filename)
# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
