import os
import secrets
from flask import render_template, redirect, request, url_for, flash, session
from cuisina_app import app
from PIL import Image
from cuisina_app.forms import ProfileForm
import cuisina_app.models as models



@app.route('/')
def sample():
  return redirect(url_for('profile', user_id=15))




@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    clear = False
    db = models.chef(user_id = user_id)
    suggested_chef = db.suggestChef()
    user = db.currentUser()
    profile = db.checkProfile()
    form = ProfileForm()
    recipe = db.userRecipes()
    session['user'] = user
    print(session['user'])
    if not profile:
      db.addProfile()
    else:
      pass
    if form.validate_on_submit() and request.method == 'POST':
      update = models.chef(first_name=form.fname.data,
                           last_name=form.lname.data,
                            age=form.age.data,
                            gender=form.register_gender.data,
                            username=form.username.data,
                            email_address=form.email.data, user_id=user_id)
     
      if update.validateUsername() == session['user'][0][1] and update.validateEmail() == session['user'][0][2]:
        clear = True
      elif update.validateUsername() != session['user'][0][1] and update.validateUsername() != 1:
        flash('Chef Username Already Exist!', 'danger')
      elif update.validateEmail() != session['user'][0][2] and update.validateEmail() != 2:
        flash('Chef Email Already Exist!', 'danger')
      elif update.validateUsername() == 1 or update.validateEmail() == 2:
        clear = True


      if clear:
        update.updateUser()
        update.updateProfile() 
        if form.upload_picture.data:
          picture_file = save_profile_picture(form.upload_picture.data)
          picture = url_for('static', filename='profile_pics/' + picture_file)
          upload_picture = models.chef(filename = picture, user_id=user_id)
          upload_picture.uploadProfilePic()
        flash('Success! Profile Saved', 'success')
      return redirect(url_for('profile', user_id=user_id))
    elif request.method == "GET":
      if len(profile) != 0:
        form.fname.data = profile[0][1]
        form.lname.data = profile[0][2]
        form.age.data = profile[0][3]
        form.register_gender.data = profile[0][4]
      else:
        form.fname.data = None
        form.lname.data = None
        form.age.data = None
      form.username.data = user[0][1]
      form.email.data = user[0][2]
    return render_template('profile.html', form=form, user=user, recipe=recipe, suggested_chef = suggested_chef)





def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)


    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




@app.route('/viewProfile/<int:user_id>')
def viewProfile(user_id):
  db = models.chef(user_id = user_id)
  suggest = models.chef(user_id = session['user'][0][1])
  user = session['user']
  other_user = db.currentUser()
  profile = db.checkProfile()
  recipe = db.userRecipes()
  suggested_chef = suggest.suggestChef()


  return render_template('userProfile.html', user = user, other_user=other_user, recipe = recipe, profile = profile, suggested_chef = suggested_chef)
