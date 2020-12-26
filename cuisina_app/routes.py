import os
import secrets
from PIL import Image
from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from cuisina_app.forms import CreatePost, addCommment, rateForm

import cuisina_app.models as models



rating = [
		{
			'rate_id': 1,
			'recipe_id': 1,
			'rate': 5
		},

		{
			'rate_id': 2,
			'recipe_id': 2,
			'rate': 4
		},

		{
			'rate_id': 3,
			'recipe_id': 3,
			'rate': 3
		},

		{
			'rate_id': 4,
			'recipe_id': 4,
			'rate': 2
		}
		
]




@app.route('/')
def filter():
	return redirect(url_for('home', fltr='All'))


@app.route('/home/<string:fltr>', methods=['GET', 'POST'])
def home(fltr):
	db = models.chef(filter=fltr)
	db.getAvgRate()
	recipe = db.viewRecipes()
	form = CreatePost()
	user = db.sampleCurrentUser()
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

	return render_template('home.html', active='home', user=user, suggested_chef=user, recipe=recipe, form=form)



@app.route('/viewpost/<int:recipe_id>', methods=['GET', 'POST'])
def viewpost(recipe_id):
	db = models.chef(recipe_id=recipe_id)
	recipe = db.viewSelectRecipe()
	user = db.sampleCurrentUser()

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
	return render_template('view-post.html',  active='home', user=user, suggested_chef=user, recipe=recipe, comments=comments, form=form, form_rate=form_rate, rate = currentRating)



@app.route('/add_rate/<recipe_id>/<rate>')
def add_rate(recipe_id, rate):
	for item in rating:
		if item['recipe_id'] == int(recipe_id):
			item['rate'] = int(rate)
	return redirect(url_for('viewpost', recipe_id=recipe_id))
	


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


@app.route('/saved_filter')
def saved_filter():
	return redirect(url_for('savedRecipe', fltr='All'))

@app.route('/savedRecipe/<string:fltr>')
def savedRecipe(fltr):
	db = models.chef(filter=fltr)
	recipe = db.viewSavedRecipes()
	user = db.sampleCurrentUser()
	return render_template('saved_recipe.html', recipe = recipe, user=user, active='saved')


@app.route('/saved/<recipe_id>')
def saveRecipe(recipe_id):
	db = models.chef(recipe_id=recipe_id)
	recipe = db.viewSelectRecipe()
	save = models.chef(saved = recipe[0][5], recipe_id=recipe_id)
	save.saveRecipe()
	return redirect(url_for('viewpost', recipe_id=recipe_id))




