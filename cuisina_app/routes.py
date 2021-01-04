import os
import secrets
from flask import render_template, redirect, request, url_for, flash, session
from datetime import timedelta
from cuisina_app import app
from PIL import Image
from cuisina_app.forms import LoginForm, SignUpForm, ProfileForm, CreatePost, addCommment, rateForm
import cuisina_app.models as models


app.permanent_session_lifetime = timedelta(days=2)

@app.route('/filter')
def filter():
  return redirect(url_for('home', fltr='All'))


@app.route('/home/<string:fltr>', methods=['GET', 'POST'])
def home(fltr):
  if 'user' in session:
    db = models.chef(filter=fltr)
    db.getAvgRate()
    recipe = db.viewRecipes()
    form = CreatePost()
    user = session['user'] 
    suggest = models.chef(user_id = session['user'][0][0])
    suggested_chef = suggest.suggestChef()
    if form.validate_on_submit() and request.method == 'POST':
      create = models.chef(title = form.title.data,
                 description = form.content.data,
                  cuisine = form.cuisine.data,
                  user_id=user[0][0])
      latest = create.addRecipes()
      if form.upload_picture.data:
        picture_file = save_picture(form.upload_picture.data)
        picture = url_for('static', filename='posted-recipe_images/' + picture_file)
        upload_picture = models.chef(filename = picture)
        upload_picture.uploadRecipePicture()
      return redirect(url_for('viewpost', recipe_id= latest))
    return render_template('home.html', active='home', user=user, suggested_chef=suggested_chef, recipe=recipe, form=form)
  else:
    return redirect(url_for('login'))



@app.route('/viewpost/<int:recipe_id>', methods=['GET', 'POST'])
def viewpost(recipe_id):
  if 'user' in session:
    db = models.chef(recipe_id=recipe_id)
    recipe = db.viewSelectRecipe()
    user = session['user']

    suggest = models.chef(user_id = session['user'][0][0]) ###
    suggested_chef = suggest.suggestChef() 

    comments = db.viewComments()

    form = addCommment()
    form_rate = rateForm()
    currentRate = models.chef(recipe_id=recipe_id, user_id=user[0][0])
    currentRating = currentRate.yourCurrentRate() 
    
    if form.validate_on_submit():
      create_comment = models.chef(content = form.comment.data, user_id=user[0][0], recipe_id=recipe_id)

      create_comment.addComment()
      return redirect(url_for('viewpost', recipe_id=recipe_id))
    elif form_rate.validate_on_submit():
      rate = models.chef(recipe_id=recipe_id, user_id=user[0][0], rating=form_rate.rate.data, isRated=currentRating)
      rate.addRate()
      return redirect(url_for('viewpost', recipe_id=recipe_id))
    return render_template('view-post.html',  active='home', user=user, suggested_chef=suggested_chef, recipe=recipe, comments=comments, form=form, form_rate=form_rate, rate = currentRating)
  else:
    return redirect(url_for('login'))



def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/posted-recipe_images', picture_fn)


  output_size = (900, 900)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn


@app.route('/saved_filter/<int:user_id>')
def saved_filter(user_id):
  return redirect(url_for('savedRecipe', user_id=user_id, fltr='All'))

@app.route('/savedRecipe/<int:user_id>/<string:fltr>')
def savedRecipe(user_id, fltr):
  db = models.chef(user_id=user_id, filter=fltr)
  recipe = db.viewSavedRecipes()
  user = session['user']
  suggest = models.chef(user_id = session['user'][0][0])
  suggested_chef = suggest.suggestChef() 
  return render_template('saved_recipe.html', recipe = recipe, user=user,suggested_chef=suggested_chef, active='saved')


@app.route('/saved/<recipe_id>/<user_id>')
def saveRecipe(recipe_id, user_id):
  db = models.chef(recipe_id=recipe_id)
  recipe = db.viewSelectRecipe()
  save = models.chef(saved = recipe[0][5], recipe_id=recipe_id, user_id=user_id)
  save.saveRecipe()
  return redirect(url_for('viewpost', recipe_id=recipe_id))

@app.route('/delete/<recipe_id>')
def deletePost(recipe_id):
  db = models.chef(recipe_id = recipe_id)
  db.deleteRecipe()
  flash('Posted Recipe Deleted Successfully!', 'success')
  return redirect(url_for('home', fltr='All'))

