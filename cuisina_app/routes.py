from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
#from cuisina_app.forms import
import cuisina_app.models as models



recipe = [
	{
		'recipe_id': '1',
		'username':'sampleUser',
		'title':'My first Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'cuisine':'Filipino',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5
	},
	{
		'recipe_id': '2',
		'username':'sampleUser2',
		'title':'My Second Recipe',
		'description': 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi',
		'status':'public',
		'cuisine':'Filipino',
		'timeDate':'December 2020',
		'comment':'sample comment',
		'rate':5
	}
]

##### SAMPLE ROUTE ###########
@app.route('/')
def sample():
	for i in recipe:
		user = i['username']
	return render_template('home.html', active='home', user=user, suggested_chef=user, recipe=recipe)


## ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE