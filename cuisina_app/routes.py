from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from PIL import Image
import sqlite3
import os
import secrets
from cuisina_app.forms import ProfileForm
import cuisina_app.models as models


##### SAMPLE ROUTE ###########
@app.route('/')
def sample():
    return render_template('layout.html', active='home', user='sampleUser07', suggested_chef='sampleChef07')


## ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE
@app.route('/profile')
def profile():
    form = ProfileForm()
    return render_template('profile.html',
                           user='sampleUser07',
                           fname='Kyle',
                           lname='Ondiano',
                           email='sample@gmail.com',
                           age='16',
                           gender='Male',
                           suggested_chef='sampleChef07',
                           form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/updateProfile', methods=["POST", "GET"])
def updateProfile():
    global first_name, last_name, email_add, aget
    form = ProfileForm()
    image_file = 'images/profile_pics/default.jpg'
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        image_file = picture_file
    else:
        image_file = 'images/profile_pics/default.jpg'
    if request.method == "POST":
        try:
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            email_add = request.form["email"]
            aget = request.form["age"]
            with sqlite3.connect("dummydata.sqlite") as conn:
                cur = conn.cursor()
                cur.execute("UPDATE profile SET fname = '{}', lname= '{}', email= '{}', age= {} WHERE user= 'sampleUser07'  ".format(first_name, last_name, email_add, aget))
                conn.commit()
        except:
            conn.rollback()
            print("fail")
        finally:
            return render_template("profile.html",
                                   user='sampleUser07',
                                   fname=first_name,
                                   lname=last_name,
                                   email=email_add,
                                   age=aget,
                                   suggested_chef='sampleChef07',
                                   image_file=image_file,
                                   form=form)
            conn.close()


@app.route('/userProfile')
def userProfile():
    return render_template('userProfile.html',
                           active='home',
                           user='sampleUser07',
                           fname='Joey Abbe',
                           lname='Abonitalla',
                           email='sample@yahoo.com',
                           age='21',
                           suggested_chef='sampleChef07')
