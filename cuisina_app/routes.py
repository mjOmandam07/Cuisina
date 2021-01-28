import os
import secrets
from flask import render_template, redirect, request, url_for, flash, session
from datetime import timedelta
from cuisina_app import app
from PIL import Image
from cuisina_app.forms import LoginForm, SignUpForm, ProfileForm, CreatePost, addCommment, rateForm
import cuisina_app.models as models


app.permanent_session_lifetime = timedelta(days=2)




@app.route('/')
def toLogin():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db = models.chef()
    if form.validate_on_submit():
        session.permanent = True
        db = models.chef(username=form.username.data,
                         password=form.password.data)

        if db.validateLogin() == 1:
            flash('Invalid Login. Chef does not exist', 'danger')
        elif db.validateLogin() == 2:
            flash('Invalid Login. Wrong Password', 'danger')
        else:
            user = db.login()
            session['user'] = user
            db = models.chef(user_id = session['user'][0][0])
            profile = db.checkProfile()
            user = db.currentUser()
            session['user'] = user
            if not profile:
              return redirect(url_for('profile', user_id=user[0][0], fltr='recipes'))
            elif not profile[0][1]:
              return redirect(url_for('profile', user_id=user[0][0], fltr='recipes'))
            else:
              return redirect(url_for('home', fltr='All'))
             
    
    if 'user' in session:
        user = session['user']
        return redirect(url_for('profile', user_id=user[0][0], fltr='recipes'))


    return render_template('login.html', form=form)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    newUser = {}
    db = models.chef()
    form = SignUpForm()
    if form.validate_on_submit():
        db = models.chef(username = form.username.data,
                         email_address = str(form.email.data),
                         password = form.password.data)
        if db.validateUsername() == 1:
            flash('Chef Username Already Exist!', 'danger')
        elif db.validateEmail() == 2:
            flash('Chef Email Already Exist!', 'danger')
        else:
            db.addNewUser()
            session.permanent = True
            login = models.chef(username=form.username.data,
                            password=form.password.data)
            user = login.login()
            session['user'] = user
            return redirect(url_for('profile', user_id=user[0][0], fltr='recipes'))
    return render_template('signUp.html', form=form)



@app.route('/profile/<int:user_id>/<string:fltr>', methods=['GET', 'POST'])
def profile(user_id, fltr):
  if 'user' in session:
    user_request = False
    if session['user'][0][0] == user_id:
      clear = False
      db = models.chef(user_id = user_id)

      suggested_chef = db.suggestChef()

      user = db.currentUser()

      profile = db.checkProfile()

      form = ProfileForm()

      friendsList = db.showFriends()

      allFriends = db.showAllFriends()

      recipe = list 

      if fltr == 'recipes':
        recipe = db.userRecipes()
      elif fltr == 'orders':
        recipe = db.userOrder()
      session['user'] = user
      suggest = models.chef(user_id = session['user'][0][0])

      friend = suggest.checkFriendReq()

      reqs = suggest.friendReq()

      if friend:
        if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
          user_request = True
        else:
          user_request = False 
      if not profile:
        db.addProfile()
        return redirect(url_for('profile', user_id=user[0][0], fltr='recipes'))
      else:
        pass
      if form.validate_on_submit() and request.method == 'POST':
        update = models.chef(first_name=form.fname.data,
                             last_name=form.lname.data,
                              age=form.age.data,
                              gender=form.register_gender.data,
                              username=form.username.data,
                              email_address=form.email.data, user_id=user_id)
       
        if update.updt_validateUsername() == session['user'][0][1] and update.updt_validateEmail() == session['user'][0][2]:
          clear = True
        elif update.updt_validateUsername() != session['user'][0][1] and update.updt_validateUsername() != 1:
          flash('Chef Username Already Exist!', 'danger')
        elif update.updt_validateEmail() != session['user'][0][2] and update.updt_validateEmail() != 2:
          flash('Chef Email Already Exist!', 'danger')
        elif update.updt_validateUsername() == 1 or update.updt_validateEmail() == 2:
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

        return redirect(url_for('profile', user_id=user_id, fltr = fltr))
      elif request.method == 'POST':
        if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
        elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('profile', user_id=user_id, fltr=fltr))
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

      return render_template('profile.html',
                               user_request=user_request, form=form,
                               fltr=fltr, user=user, 
                               recipe=recipe, suggested_chef = suggested_chef, 
                               active='profile', profile = profile,
                               friendsList = friendsList, allFriends=allFriends,
                               reqs=reqs)
    else:
      flash('Please Logout and Login to your desired account', 'info')
      return redirect(url_for('login'))
  else:
    return redirect(url_for('login'))


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


@app.route('/viewProfile/<int:user_id>/<string:fltr>', methods=['GET', 'POST'])
def viewProfile(user_id, fltr):
  if 'user' in session:
    user_request = False
    isRequest = False
    other_request = False
    isFrnd = False

    db = models.chef(user_id = user_id)
    suggest = models.chef(user_id = session['user'][0][0])

    user = session['user']
    other_user = db.currentUser()
    profile = db.checkProfile()

    recipe = list

    friend = suggest.checkFriend()
    viewedFriend = db.checkViewdReq()
    friendReq = suggest.checkFriendReq()

    friendCheck = models.chef(user_id=user_id, other_user=session['user'][0][0])

    isfren = friendCheck.isFriend()

    friendsList = db.showFriends()

    allFriends = db.showAllFriends()

    if isfren:
      if isfren[0][4] == 1:
        isFrnd = True
      elif isfren[0][4] != 1 and isfren[0][2] != session['user'][0][0]:
        isRequest = True
      elif isfren[0][2] == session['user'][0][0]:
        other_request = True


    
    if friendReq:
        if friendReq[0][2] == session['user'][0][0] and friendReq[0][3] == 0:
          user_request = True
        else:
          user_request = False
    if fltr == 'recipes':
      recipe = db.userRecipes()
    elif fltr == 'orders':
      recipe = db.userOrder()
    suggested_chef = suggest.suggestChef()

    if request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('viewProfile', user_id=user_id, fltr=fltr))

    return render_template('userProfile.html', isFrnd = isFrnd, other_request=other_request,
                                              user_request=user_request, request=isRequest,
                                              fltr=fltr, user = user, active='profile',
                                              other_user=other_user, recipe = recipe,
                                              profile = profile, suggested_chef = suggested_chef,
                                              friendsList = friendsList, allFriends = allFriends)

  else:
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('login'))


@app.route('/filter')
def filter():
  return redirect(url_for('home', fltr='All'))


@app.route('/home/<string:fltr>', methods=['GET', 'POST'])
def home(fltr):
  if 'user' in session:
    user_request = False
    db = models.chef(filter=fltr)
    db.getAvgRate()
    recipe = db.viewRecipes()
    form = CreatePost()
    user = session['user'] 
    suggest = models.chef(user_id = session['user'][0][0])
    friend = suggest.checkFriendReq()
    if friend:
      if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
        user_request = True
      else:
        user_request = False 
    profile = suggest.currentUser()
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
    elif request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('filter')) 
      return redirect(url_for('viewpost', recipe_id= latest))
    return render_template('home.html', active='home', user_request = user_request, user=user, suggested_chef=suggested_chef, recipe=recipe, form=form, fltr=fltr, profile=profile)
  else:
    return redirect(url_for('login'))



@app.route('/viewpost/<int:recipe_id>', methods=['GET', 'POST'])
def viewpost(recipe_id):
  if 'user' in session:
    user_request = False
    db = models.chef(recipe_id=recipe_id)
    recipe = db.viewSelectRecipe()
    user = session['user']
    suggest = models.chef(user_id = session['user'][0][0])
    friend = suggest.checkFriendReq()
    if friend:
      if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
        user_request = True
      else:
        user_request = False 
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
    elif request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('viewpost', recipe_id=recipe_id))
    return render_template('view-post.html',  active='home',user_request=user_request, user=user, suggested_chef=suggested_chef, recipe=recipe, comments=comments, form=form, form_rate=form_rate, rate = currentRating)
  else:
    return redirect(url_for('login'))



@app.route('/orderfilter')
def orderfilter():
  return redirect(url_for('ordersFeed', fltr='All'))



@app.route('/orders/<string:fltr>', methods=['GET', 'POST'])
def ordersFeed(fltr):
  if 'user' in session:
    user_request = False
    db = models.chef(filter=fltr)
    db.getAvgRate()
    recipe = db.viewOrder()
    form = CreatePost()
    user = session['user'] 
    suggest = models.chef(user_id = session['user'][0][0])
    suggested_chef = suggest.suggestChef()
    friend = suggest.checkFriendReq()
    if friend:
      if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
        user_request = True
      else:
        user_request = False 
    if form.validate_on_submit() and request.method == 'POST':
      create = models.chef(title = form.title.data,
                 description = form.content.data,
                  cuisine = form.cuisine.data,
                  user_id=user[0][0])
      latest = create.addOrder()
      if form.upload_picture.data:
        picture_file = save_picture(form.upload_picture.data)
        picture = url_for('static', filename='posted-recipe_images/' + picture_file)
        upload_picture = models.chef(filename = picture)
        upload_picture.uploadOrderPic()
      return redirect(url_for('viewOrder', recipe_id= latest))
    elif request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('orderfilter'))
    return render_template('ordersfeed.html', user_request=user_request, active='order', user=user, suggested_chef=suggested_chef, recipe=recipe, form=form, fltr=fltr)
  else:
    return redirect(url_for('login'))



@app.route('/viewOrder/<int:recipe_id>', methods=['GET', 'POST'])
def viewOrder(recipe_id):
  if 'user' in session:
    user_request = False
    db = models.chef(recipe_id=recipe_id)
    recipe = db.viewSelectOrders()
    user = session['user']

    suggest = models.chef(user_id = session['user'][0][0]) ###
    suggested_chef = suggest.suggestChef() 

    friend = suggest.checkFriendReq()
    if friend:
      if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
        user_request = True
      else:
        user_request = False 

    comments = db.viewOrderComment()

    form = addCommment()

    currentRate = models.chef(recipe_id=recipe_id, user_id=user[0][0])
    currentRating = currentRate.yourCurrentRate() 
    
    if form.validate_on_submit():
      create_comment = models.chef(content = form.comment.data, user_id=user[0][0], recipe_id=recipe_id)

      create_comment.addOrderComment()
      return redirect(url_for('viewOrder', recipe_id=recipe_id))
    elif request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('viewOrder', recipe_id=recipe_id))
    
    return render_template('view-order.html',  user_request=user_request, active='order', user=user, suggested_chef=suggested_chef, recipe=recipe, comments=comments, form=form)
  else:
    return redirect(url_for('login'))




@app.route('/hotfilter')
def hotfilter():
  return redirect(url_for('hot', fltr='All'))


@app.route('/hot/<string:fltr>', methods=['GET', 'POST'])
def hot(fltr):
  if 'user' in session:
    user_request = False
    db = models.chef(filter=fltr)
    db.getAvgRate()
    recipe = db.viewHotRecipes()
    form = CreatePost()
    user = session['user'] 
    suggest = models.chef(user_id = session['user'][0][0])
    friend = suggest.checkFriendReq()
    if friend:
      if friend[0][2] == session['user'][0][0] and friend[0][3] == 0:
        user_request = True
      else:
        user_request = False 
    profile = suggest.currentUser()
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
    elif request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('filter')) 
      return redirect(url_for('viewpost', recipe_id= latest))
    return render_template('home.html', active='hot', user_request = user_request, user=user, suggested_chef=suggested_chef, recipe=recipe, form=form, fltr=fltr, profile=profile)
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
  if request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr='posts'))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('saved_filter', user_id=user_id))
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



@app.route('/deleteOrder/<recipe_id>')
def deleteOrder(recipe_id):
  db = models.chef(recipe_id = recipe_id)
  db.deleteOrder()
  flash('Order Deleted Successfully!', 'success')
  return redirect(url_for('ordersFeed', fltr='All'))



@app.route('/acceptFriend/<current_user>/<other_user>')
def acceptFriend(current_user, other_user):
    db = models.chef(user_id = current_user)
    db.acceptFriend()


    return redirect(url_for('viewProfile', user_id = other_user, fltr='recipes'))



@app.route('/addFriend/<current_user>/<other_user>')
def addFriend(current_user, other_user):
    db = models.chef(user_id = current_user, other_user=other_user)
    db.addFriend()


    return redirect(url_for('viewProfile', user_id = other_user, fltr='recipes'))




@app.route('/removeFriend/<current_user>/<other_user>')
def removeFriend(current_user, other_user):
    db = models.chef(user_id = current_user, other_user=other_user)
    db.removeFriend()

    return redirect(url_for('viewProfile', user_id = other_user, fltr='recipes'))




@app.route('/search/<search_content>/<fltr>', methods=['GET', 'POST'])
def search(search_content, fltr):
  if 'user' in session:
    user = session['user']
    db = models.chef(title=search_content)

    suggest = models.chef(user_id = session['user'][0][0], username=search_content)
    suggested_chef = suggest.suggestChef()

    recipe = db.searchRecipe()
    search_user = suggest.searchUser()
    if request.method == 'POST':
      if request.form["search"]:
            search_content = request.form["search"]
            return redirect(url_for('search', search_content=search_content, fltr=fltr))
      elif not request.form["search"]:
            flash('Please Search recipe or chef', 'danger')
            return redirect(url_for('search', search_content=search_content, fltr=fltr))
  else:
    return redirect(url_for('login'))
  return render_template('search.html',search_content=search_content, user=user, recipe=recipe,search_user=search_user, suggested_chef =suggested_chef, fltr=fltr)
