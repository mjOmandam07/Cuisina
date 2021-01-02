from cuisina_app import mysql
class chef(object):
	def __init__(self, user_id=None, username=None,
				 password=None, email_address=None):

		self.user_id = user_id
		self.username = username
		self.password = password
		self.email_address = email_address


	def getUserId(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT user_id FROM user where username = '{}'".format(self.username)


		cursor.execute(sql)
		display = cursor.fetchall()
		return display


	def login(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE username = '{}' and password = '{}'".format(self.username, self.password)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display

	def addNewUser(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO user(username, email_address, password)
					VALUES ('%s', '%s', '%s')""" % (self.username, self.email_address, self.password)

		cursor.execute(sql)
		mysql.connection.commit() 


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

		cursor.execute(sql)
		display = cursor.fetchall()

		return display


	def validateUsername(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE username = '{}'".format(self.username)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			return 1

	def viewUser(self):
		cursor = mysql.connection.cursor()

		sql = "SELECT * FROM user WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		return display

	def validateEmail(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE email_address = '{}'".format(self.email_address)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			return 2
		else:
			return 0
		

