from cuisina_app import mysql
class chef(object):
	def __init__(self, user_id=None, username=None,
				 password=None, email_address=None):

		self.user_id = user_id
		self.username = username
		self.password = password
		self.email_address = email_address



##############SAMPLE QUERY######################
	def allUser(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT * FROM user"

		cursor.execute(sql)
		display = cursor.fetchall()
		return display
################################################


	def addNewUser(self):
		cursor = mysql.connection.cursor()
		sql = """INSERT INTO user(username, email_address, password)
					VALUES ('%s', '%s', '%s')""" % (self.username, self.email_address, self.password)

		cursor.execute(sql)
		mysql.connection.commit() 

	def viewUser(self):
		cursor = mysql.connection.cursor()

		sql = "SELECT * FROM user WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()
		return display

	def validateUser(self):
		cursor = mysql.connection.cursor()
		sql = "SELECT username FROM user WHERE username = '{}' and email_address = '{}'".format(self.username, self.email_address)

		cursor.execute(sql)
		display = cursor.fetchall()
		for item in display:
			if item[1] == self.username or item[2] == self.email_address:
				return True 