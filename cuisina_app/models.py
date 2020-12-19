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



	def addNewUser(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO user(username, email_address, password)
					VALUES ('%s', '%s', '%s')""" % (self.username, self.email_address, self.password)

		cursor.execute(sql)
		mysql.connection.commit() 

	def viewUser(self):
		cursor = mysql.connection.cursor()

		sql = "SELECT * FROM user WHERE username = '{}'".format(self.username)

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

	def validateEmail(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user WHERE email_address = '{}'".format(self.email_address)

		cursor.execute(sql)
		display = cursor.fetchall()
		
		if display:
			return 2
		else:
			return 0
		
