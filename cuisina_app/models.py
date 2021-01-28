from cuisina_app import mysql
from datetime import datetime



class chef(object):
	def __init__(self, filter=None, user_id=None, username=None, password=None, email_address=None,
					first_name=None, last_name=None, age = None, gender = None,

					recipe_id=None, title=None, description=None, status=None, time_date=None, cuisine=None, saved=None,

					comment_id=None, content=None,   ###  arranged

					rate_id=None, rating = None, isRated = None,

					image_id=None,

					filename = None,
					other_user = None): 


		self.filter = filter

		self.user_id = user_id
		self.other_user = other_user
		self.username = username
		self.password = password
		self.email_address = email_address

		self.first_name = first_name
		self.last_name = last_name
		self.age = age
		self.gender = gender


		self.recipe_id = recipe_id
		self.title = title
		self.description = description
		self.status = status
		self.time_date = datetime.now()
		self.cuisine = cuisine
		self.saved = saved

		self.comment_id = comment_id
		self.content = content

		self.rate_id = rate_id
		self.rating = rating
		self.isRated = isRated

		self.image_id = image_id
		self.filename = filename



	def addNewUser(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO user(username, email_address, password)
					VALUES ('%s', '%s', '%s')""" % (self.username, self.email_address, self.password)

		cursor.execute(sql)
		mysql.connection.commit() 


	def validateUsername(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE username = '{}'".format(self.username)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			return 1
			

	def validateEmail(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE email_address = '{}'".format(self.email_address)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			return 2
		else:
			return 0



	def login(self):
		cursor = mysql.connection.cursor()

		sql = "SELECT * FROM user WHERE username = '{}' and password = '{}'".format(self.username, self.password)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display




	def validateLogin(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE username = '{}'".format(self.username)

		cursor.execute(sql)
		display = cursor.fetchall()
		if display:
			for item in display:
				if item[3] != self.password:
					return 2
				else:
					return 0
		elif not display:
			return 1
		else:
			return 0


##################### Profile #########################################


	def currentUser(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT u.*,i.filename FROM 
		            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
		                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display



	def suggestChef(self):
		cursor = mysql.connection.cursor()
		max_prof_id = self.user_id

		while max_prof_id == self.user_id:
		    sql = """SELECT user_id FROM profile order by rand() limit 1"""



		    cursor.execute(sql)
		    display = cursor.fetchall()
		    
		    max_prof_id = display[0][0]


		sql2 = """SELECT u.*,i.filename FROM 
		        ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
		            LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(max_prof_id)


		cursor.execute(sql2)
		suggest = cursor.fetchall()

		return suggest

  
    
	def checkProfile(self):
	    cursor = mysql.connection.cursor()
	    sql = "SELECT * FROM profile WHERE user_id = {}".format(self.user_id)

	    cursor.execute(sql)
	    display = cursor.fetchall()
	    return display



	def userRecipes(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
						WHERE r.user_id = {} ORDER BY r.time_date""".format(self.user_id)


		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts

		cursor.execute(sql)
		display = cursor.fetchall()
		return display


	def userOrder(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
						WHERE r.user_id = {} ORDER BY r.time_date""".format(self.user_id)


		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts

		cursor.execute(sql)
		display = cursor.fetchall()
		return display



	
	def addProfile(self):
		cursor = mysql.connection.cursor()
		sql = "INSERT INTO profile(user_id) VALUES ('%d')" % (self.user_id)

		cursor.execute(sql)
		mysql.connection.commit()

		sql2 = "SELECT profile_id FROM profile WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql2)
		display = cursor.fetchall()

		sql3 = """INSERT INTO images (filename, profile_id) VALUES ('%s', %d)""" % ('/static/profile_pics/default.jpg', display[0][0])

		cursor.execute(sql3)
		mysql.connection.commit()



	def uploadProfilePic(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT profile_id FROM profile WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		sql2 = """SELECT filename FROM images WHERE profile_id = {}""".format(display[0][0])

		cursor.execute(sql2)
		filename = cursor.fetchall()

		if len(filename) == 0:
			sql3 = """INSERT INTO images (filename, profile_id) VALUES ('%s', %d)""" % (self.filename, display[0][0])
		else:
			sql3 = """UPDATE images SET filename = '{}' WHERE profile_id = {}""".format(self.filename, display[0][0])

		cursor.execute(sql3)
		mysql.connection.commit()


	def updateProfile(self):
		cursor = mysql.connection.cursor()
		sql = """UPDATE profile SET first_name = '{}', last_name = '{}', birthday = '{}', gender = '{}' 
		            WHERE user_id = {}""".format(self.first_name, self.last_name, self.age, self.gender, self.user_id)

		cursor.execute(sql)
		mysql.connection.commit()

	def updateUser(self):
		cursor = mysql.connection.cursor()
		sql = """ UPDATE user SET username = '{}', email_address = '{}' WHERE user_id = {}""".format(self.username, self.email_address, self.user_id)

		cursor.execute(sql)
		mysql.connection.commit()



	def updt_validateUsername(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT username FROM user WHERE username = '{}'".format(self.username)

		cursor.execute(sql)
		display = cursor.fetchall()

		if display:
			return display[0][0]
		else:
			return 1


	def updt_validateEmail(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT email_address FROM user WHERE email_address = '{}'".format(self.email_address)

		cursor.execute(sql)
		display = cursor.fetchall()

		if display:
			return display[0][0]
		else:
			return 2


	def searchUser(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT u.user_id, u.username, p.first_name, p.last_name,i.filename FROM 
		            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
		                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.username = '{}';""".format(self.username)

			
		cursor.execute(sql)
		display = cursor.fetchall()

		return display




############################ POST-RECIPES #####################


	def viewRecipes(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """"""

		if self.filter == 'All':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	 ORDER BY r.time_date DESC"""

			
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Western':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Western' ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Asian':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Asian' ORDER BY r.time_date DESC"""


			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'European':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'European' ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts
			
		elif self.filter == 'Filipino':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Filipino' ORDER BY r.time_date DESC"""
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts

	def viewHotRecipes(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """"""

		if self.filter == 'All':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id) WHERE r.avg_rating > 4
					 	 	 ORDER BY r.time_date DESC"""

			
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Western':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Western' AND r.avg_rating > 4 ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Asian':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Asian' AND r.avg_rating > 4 ORDER BY r.time_date DESC"""


			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'European':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'European' AND r.avg_rating > 4 ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts
			
		elif self.filter == 'Filipino':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Filipino' AND r.avg_rating > 4 ORDER BY r.time_date DESC"""
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts			


	def viewOrder(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """"""

		if self.filter == 'All':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	 ORDER BY r.time_date DESC"""

			
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Western':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Western' ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'Asian':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Asian' ORDER BY r.time_date DESC"""


			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		elif self.filter == 'European':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'European' ORDER BY r.time_date DESC"""

			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts
			
		elif self.filter == 'Filipino':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE cuisine = 'Filipino' ORDER BY r.time_date DESC"""
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()
				posts.append(item + (display[0][4],))

			return posts




	def viewSelectRecipe(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 JOIN user AS u ON u.user_id = r.user_id) WHERE r.recipe_id = '{}'""".format(self.recipe_id)
		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts

	def viewSelectOrders(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM ((images AS i RIGHT JOIN order_recipe as r ON i.order_id = r.recipe_id )
					 JOIN user AS u ON u.user_id = r.user_id) WHERE r.recipe_id = '{}'""".format(self.recipe_id)
		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts



	def uploadRecipePicture(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT recipe_id FROM recipe WHERE recipe_id = (SELECT max(recipe_id) FROM recipe)"""

		cursor.execute(sql)
		display = cursor.fetchall()


		sql2 = """INSERT INTO images (filename, recipe_id) VALUES ('%s', %d)""" % (self.filename, display[0][0])

		cursor.execute(sql2)
		mysql.connection.commit()

	def uploadOrderPic(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT recipe_id FROM order_recipe WHERE recipe_id = (SELECT max(recipe_id) FROM order_recipe)"""

		cursor.execute(sql)
		display = cursor.fetchall()


		sql2 = """INSERT INTO images (filename, order_id) VALUES ('%s', %d)""" % (self.filename, display[0][0])

		cursor.execute(sql2)
		mysql.connection.commit()




	def addRecipes(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO recipe (title, description, time_date, cuisine, user_id)
					 VALUES ('%s', '%s', '%s','%s',%d)""" % (self.title,
					 													self.description, 
					 													 self.time_date,
					 													 self.cuisine, 
					 													 self.user_id)
	
		cursor.execute(sql)
		mysql.connection.commit()

		sql2 = """SELECT recipe_id FROM recipe WHERE recipe_id = (SELECT max(recipe_id) FROM recipe)"""

		cursor.execute(sql2)
		display = cursor.fetchall()

		return display[0][0]

	def addOrder(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO order_recipe (title, description, time_date, cuisine, user_id)
					 VALUES ('%s', '%s', '%s','%s',%d)""" % (self.title,
					 													self.description, 
					 													 self.time_date,
					 													 self.cuisine, 
					 													 self.user_id)
	
		cursor.execute(sql)
		mysql.connection.commit()

		sql2 = """SELECT recipe_id FROM order_recipe WHERE recipe_id = (SELECT max(recipe_id) FROM order_recipe)"""

		cursor.execute(sql2)
		display = cursor.fetchall()


		print(display[0][0])
		return display[0][0]


	def deleteRecipe(self):
		cursor = mysql.connection.cursor()

		sql = """DELETE FROM recipe WHERE recipe_id = {}""".format(self.recipe_id)

		cursor.execute(sql)
		mysql.connection.commit()


	def deleteOrder(self):
		cursor = mysql.connection.cursor()

		sql = """DELETE FROM order_recipe WHERE recipe_id = {}""".format(self.recipe_id)

		cursor.execute(sql)
		mysql.connection.commit()


	def deleteOrder(self):
		cursor = mysql.connection.cursor()

		sql = """DELETE FROM order_recipe WHERE recipe_id = {}""".format(self.recipe_id)

		cursor.execute(sql)
		mysql.connection.commit()



	def saveRecipe(self):
		cursor = mysql.connection.cursor()

		if self.saved == 0:
			sql = """ UPDATE recipe SET saved = TRUE, saved_by = {} WHERE recipe_id = '{}' """.format(self.user_id, self.recipe_id)
		else:
			sql = """ UPDATE recipe SET saved = FALSE, saved_by = '{}' WHERE recipe_id = '{}' """.format(0, self.recipe_id)
			

		cursor.execute(sql)
		mysql.connection.commit()



	def viewSavedRecipes(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """"""
		if self.filter == 'All':
			sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	WHERE r.saved_by = {} ORDER BY r.time_date DESC""".format(self.user_id)

			
			cursor.execute(sql)
			recipes = cursor.fetchall()

			for item in recipes:
				sql2 = """SELECT u.*,i.filename FROM 
					            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
					                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

				cursor.execute(sql2)
				display = cursor.fetchall()

				posts.append(item + (display[0][4],))

			return posts

		

	def viewComments(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """ SELECT c.*, u.username FROM can_comment as c JOIN user as u ON c.user_id = u.user_id WHERE recipe_id = '{}' """.format(self.recipe_id)

		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[3])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts




	def addComment(self):
		cursor = mysql.connection.cursor()

		sql = """ INSERT INTO can_comment(content, time_date, user_id, recipe_id)
					VALUES('{}', '{}', {}, {}) """.format(self.content, self.time_date, self.user_id, self.recipe_id)


		cursor.execute(sql)
		mysql.connection.commit()



	def viewOrderComment(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """ SELECT c.*, u.username FROM can_comment as c JOIN user as u ON c.user_id = u.user_id WHERE order_id = '{}' """.format(self.recipe_id)

		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[3])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts




	def addOrderComment(self):
		cursor = mysql.connection.cursor()

		sql = """ INSERT INTO can_comment(content, time_date, user_id, order_id)
					VALUES('{}', '{}', {}, {}) """.format(self.content, self.time_date, self.user_id, self.recipe_id)


		cursor.execute(sql)
		mysql.connection.commit()




	def addRate(self):
		cursor = mysql.connection.cursor()

		sql=""""""

		if self.isRated:
			sql = """UPDATE can_rate SET rating = '{}'
					WHERE  user_id = '{}' AND recipe_id = '{}'""".format(self.rating, self.user_id, self.recipe_id)
		else:
			sql = """INSERT INTO can_rate(rating, user_id, recipe_id)
					VALUES('%s', %d, %d)""" % (self.rating, self.user_id, self.recipe_id)

		cursor.execute(sql)
		mysql.connection.commit()


	def yourCurrentRate(self):
		cursor = mysql.connection.cursor()

		sql = """SELECT rating FROM can_rate WHERE recipe_id = '{}' AND user_id = '{}'""".format(self.recipe_id,self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display



	def getAvgRate(self):
		rates = []
		rates.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id)
					 	 	 ORDER BY r.time_date"""


		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = "SELECT rating FROM can_rate WHERE recipe_id = {}".format(item[0])

			cursor.execute(sql2)
			display = cursor.fetchall()

			for rate in display:
				rates.append(rate[0])
				get_avg = sum(rates) / len(rates)
				average_rate = round(get_avg)
				
				sql3 = """UPDATE recipe SET avg_rating = '{}'
					WHERE recipe_id = '{}'""".format(average_rate, item[0])

				cursor.execute(sql3)
				mysql.connection.commit()
				rates.clear()



	def searchRecipe(self):
		posts = []
		posts.clear()
		cursor = mysql.connection.cursor()
		sql = """SELECT r.*,i.filename, u.username FROM
					 ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
					 	 JOIN user AS u ON u.user_id = r.user_id) WHERE r.title = '{}'
					 	 	 ORDER BY r.time_date DESC""".format(self.title)

			
		cursor.execute(sql)
		recipes = cursor.fetchall()

		for item in recipes:
			sql2 = """SELECT u.*,i.filename FROM 
				            ((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
				                 LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[7])

			cursor.execute(sql2)
			display = cursor.fetchall()

			posts.append(item + (display[0][4],))

		return posts




############################## FRIEND SECT ###########################	

	def addFriend(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO friends(requester_id, addressee_id) VALUES ('{}', '{}')""".format(self.user_id, self.other_user)

		cursor.execute(sql)
		mysql.connection.commit()
	


	def checkFriend(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT * FROM friends WHERE requester_id = '{}'""".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		return display


	def checkViewdReq(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT * FROM friends WHERE requester_id = '{}'""".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		return display

	def checkFriendReq(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT * FROM friends WHERE addressee_id = '{}'""".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		
		return display


	def isFriend(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT * FROM friends WHERE requester_id = '{}' and addressee_id = '{}'""".format(self.user_id, self.other_user)

		cursor.execute(sql)
		display = cursor.fetchall()
		if display:
			return display

		sql2 = """SELECT * FROM friends WHERE requester_id = '{}' and addressee_id = '{}'""".format(self.other_user, self.user_id)
		cursor.execute(sql2)
		display2 = cursor.fetchall()

		if display2:
			return display2


	def acceptFriend(self):
		cursor = mysql.connection.cursor()
		sql = """UPDATE friends SET status = 1, isFriend = True WHERE addressee_id = '{}'""".format(self.user_id)

		cursor.execute(sql)
		mysql.connection.commit()


	

	def removeFriend(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT * FROM friends WHERE requester_id = '{}' and addressee_id = '{}'""".format(self.user_id, self.other_user)

		cursor.execute(sql)
		display = cursor.fetchall()
		if display:
			inSql = """DELETE FROM friends WHERE id = '{}'""".format(display[0][0])
			cursor.execute(inSql)
			mysql.connection.commit()




		sql2 = """SELECT * FROM friends WHERE requester_id = '{}' and addressee_id = '{}'""".format(self.other_user, self.user_id)
		cursor.execute(sql2)
		display2 = cursor.fetchall()
		if display2:
			inSql2 = """DELETE FROM friends WHERE id = '{}'""".format(display2[0][0])
			cursor.execute(inSql2)
			mysql.connection.commit()


	def showFriends(self):
		friends = []
		friends.clear()
		cursor = mysql.connection.cursor()
		user = self.user_id

		sql = """SELECT * FROM friends WHERE (requester_id = '{}' OR addressee_id = '{}') AND isFriend = 1 LIMIT 6""".format(self.user_id, user)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			for item in display:
				if item[1] != self.user_id:
					print("\n",item[1],"requester_id")
					sql2 = """SELECT u.user_id, u.username, i.filename FROM 
									((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
			                 					LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[1])
					cursor.execute(sql2)
					display2 = cursor.fetchall()
					print(display2[0], "\n")
					friends.append(display2[0])

				if item[2] != self.user_id:
					print(item[2],"addressee")
					sql3 = """SELECT u.user_id, u.username, i.filename FROM 
									((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
												LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[2])
					cursor.execute(sql3)
					display3 = cursor.fetchall()
					print(display3[0],"\n")
					friends.append(display3[0])

		return friends

				


	def showAllFriends(self):
		friends = []
		friends.clear()
		cursor = mysql.connection.cursor()
		user = self.user_id

		sql = """SELECT * FROM friends WHERE (requester_id = '{}' OR addressee_id = '{}') AND isFriend = 1""".format(self.user_id, user)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			for item in display:
				if item[1] != self.user_id:
					print("\n",item[1],"requester_id")
					sql2 = """SELECT u.user_id, u.username, i.filename FROM 
									((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
			                 					LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[1])
					cursor.execute(sql2)
					display2 = cursor.fetchall()

					friends.append(display2[0])

				if item[2] != self.user_id:
					print(item[2],"addressee")
					sql3 = """SELECT u.user_id, u.username, i.filename FROM 
									((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
												LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[2])
					cursor.execute(sql3)
					display3 = cursor.fetchall()

					friends.append(display3[0])

					
		return friends



	def friendReq(self):
		friendReq = []
		friendReq.clear()
		cursor = mysql.connection.cursor()
		user = self.user_id

		sql = """SELECT * FROM friends WHERE addressee_id = '{}' AND isFriend = 0""".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			for item in display:
				sql2 = """SELECT u.user_id, u.username, i.filename FROM 
								((user as u LEFT JOIN profile as p ON u.user_id = p.user_id)
			                 				LEFT JOIN images AS i ON i.profile_id = p.profile_id) WHERE u.user_id = {}""".format(item[1])
				cursor.execute(sql2)
				display2 = cursor.fetchall()
				friendReq.append(display2[0])

		return friendReq


	def checkRank(self):

		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM points WHERE user_id = '{}'".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display[0][0]


	def masterChef(self):

		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM points WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display[0][0]









		