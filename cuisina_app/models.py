from cuisina_app import mysql


class chef(object):
	def __init__(self, user_id=None, username=None,
				 password=None, email_address=None):

		self.user_id = user_id
		self.username = username
		self.password = password
		self.email_address = email_address



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



	def viewUser(self):
		cursor = mysql.connection.cursor()

		sql = "SELECT * FROM user WHERE user_id = {}".format(self.user_id)

		cursor.execute(sql)
		display = cursor.fetchall()

		return display