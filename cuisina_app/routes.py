from flask import render_template, redirect, request, url_for, flash, jsonify
from cuisina_app import app
#from cuisina_app.forms import
import cuisina_app.models as models


##### SAMPLE ROUTE ###########
@app.route('/')
def sample():
	return render_template('layout.html', active='home', user='sampleUser07', suggested_chef='sampleChef07')


## ADD THE ROUTE/ROUTES OF/FOR YOUR FEATURE