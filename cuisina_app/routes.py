import os
import secrets
from PIL import Image
from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
from cuisina_app.forms import CreatePost, addCommment

import cuisina_app.models as models



recipe = [
	{
		'recipe_id': 1,
		'username':'sampleUser',
		'title':'My first Western Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'saved':False,
		'cuisine':'Western',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5,
		'image': '/static/images/default.jpg',
	},
	{
		'recipe_id': 2,
		'username':'sampleUser2',
		'title':'My Second Asian Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'saved':False,
		'cuisine':'Asian',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5,
		'image':None,
	},
	{
		'recipe_id': 3,
		'username':'sampleUser2',
		'title':'My Second European Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'saved':False,
		'cuisine':'European',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5,
		'image':None,
	},
	{
		'recipe_id': 4,
		'username':'sampleUser2',
		'title':'My Second  Filipino Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'saved':True,
		'cuisine':'Filipino',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5,
		'image':None,
	}
]



comments=[
	{
		'user':'commentor1',
		'recipe_id':1,
		'content': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'timeDate':'December 2020'
	},

	{
		'user':'commentor2',
		'recipe_id':2,
		'content': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'timeDate':'December 2020'
	}
]

saved = []

@app.route('/')
def filter():
	return redirect(url_for('home', fltr='All'))


@app.route('/home/<string:fltr>', methods=['GET', 'POST'])
def home(fltr):
	recipe_to_view = []

	for i in recipe:
		user = i['username']
		if fltr != 'All':
			if i['cuisine'] == fltr:
				recipe_to_view.append(i)
		else:
			recipe_to_view = recipe
	lastpost = recipe[-1]
	last_id = lastpost['recipe_id']
	form = CreatePost()
	newPost = {
		'recipe_id': last_id + 1,
		'username':user,
		'title':'',
		'description': '',
		'status':'public',
		'cuisine':'Filipino',
		'timeDate':'December 2020',
		'rate':5,
		'image':None
	}

	
	if form.validate_on_submit() and request.method == 'POST':
		newPost['title'] = form.title.data
		newPost['description'] = form.content.data
		newPost['cuisine'] = form.cuisine.data
		if form.upload_picture.data:
			picture_file = save_picture(form.upload_picture.data)
			newPost['image'] = url_for('static', filename='user_images/' + picture_file)
		recipe.append(newPost)
		return redirect(url_for('viewpost', recipe_id=newPost['recipe_id']))

	return render_template('home.html', active='home', user=user, suggested_chef=user, recipe=recipe_to_view, form=form)



@app.route('/viewpost/<int:recipe_id>', methods=['GET', 'POST'])
def viewpost(recipe_id):
	lastpost = {}
	user = str
	comment_to_view = []

	for item in comments:
		if item['recipe_id'] == recipe_id:
			comment_to_view.append(item)

	for i in recipe:
		if i['recipe_id'] == recipe_id:
			lastpost = i
			user = lastpost['username']
	newComment = {
		'user': user,
		'recipe_id':lastpost['recipe_id'],
		'content':'',
		'timeDate':'December 2020'
	}
	form = addCommment()
	
	if form.validate_on_submit() and request.method == 'POST':
		newComment['content'] = form.comment.data
		comments.append(newComment)
		return redirect(url_for('viewpost', recipe_id=lastpost['recipe_id']))

	return render_template('view-post.html',  active='home', user=user, suggested_chef=user, recipe=lastpost, comments=comment_to_view, form=form)



def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/user_images', picture_fn)


	output_size = (900, 900)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn



@app.route('/savedRecipe')
def savedRecipe():
	for i in recipe:
		user = i['username']
		if i['saved'] == True:
			saved.append(i)
	return render_template('saved_recipe.html', user=user, recipe = saved)


@app.route('/saved/<int:recipe_id>')
def saved(recipe_id):

	saved = []
	for i in recipe:
		if i['recipe_id'] == recipe_id:
			saved.append(i)
	return jsonify({'recipe' : saved})



