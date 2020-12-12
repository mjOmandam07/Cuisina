from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
#from cuisina_app.forms import
import cuisina_app.models as models



recipe = [
	{'recipe_id': '1',
	'user_name':'sampleUser',
	'description':'My first Recipe',
	'status':'public',
	'cuisine':'Filipino',
	'timeDate':'December 2020',
	'comment':'sample comment',
	'rate':5}
]

##### SAMPLE ROUTE ###########
@app.route('/')
def sample():
	return ("<h1>Hello CUISINA World</h1>")


## ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE