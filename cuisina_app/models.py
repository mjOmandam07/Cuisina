from cuisina_app import mysql
from datetime import datetime



class chef(object):
	def __init__(self, filter=None, user_id=None, username=None, password=None, email_address=None,
					first_name=None, last_name=None, age = None, gender = None,

					recipe_id=None, title=None, description=None, status=None, time_date=None, cuisine=None, saved=None,

					comment_id=None, content=None,   ###  arranged

					rate_id=None, rating = None, isRated = None,

					image_id=None,

					filename = None): 


		self.filter = filter

		self.user_id = user_id
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


	def uploadRecipePicture(self):
		cursor = mysql.connection.cursor()
		sql = """SELECT recipe_id FROM recipe WHERE recipe_id = (SELECT max(recipe_id) FROM recipe)"""

		cursor.execute(sql)
		display = cursor.fetchall()


		sql2 = """INSERT INTO images (filename, recipe_id) VALUES ('%s', %d)""" % (self.filename, display[0][0])

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


	def deleteRecipe(self):
		cursor = mysql.connection.cursor()

		sql = """DELETE FROM recipe WHERE recipe_id = {}""".format(self.recipe_id)

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


		
		