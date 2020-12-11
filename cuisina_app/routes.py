from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
#from cuisina_app.forms import
import cuisina_app.models as models


##### SAMPLE ROUTE ###########
@app.route('/')
def sample():
	return ("<h1>Hello CUISINA World</h1>")


## ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE