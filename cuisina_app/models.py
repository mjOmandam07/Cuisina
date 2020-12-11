from cuisina_app import mysql


''' 

	HERE WE CAN PUT OUR SQL QUERIES WE CAN ADD OR REMOVE A QUERY

	GIVEN THAT YOU HAVE ENOUGH KNOWLEDGE OF THE OTHER FEATURES


	YOU CAN ADD OR REMOVE QUERY ONLY BASING ON THE  FEATURE YOU ARE DOING


	THE CURRENT VARIABLES/ATTRIBUTES ARE THE VARIABLE/ATTRIBUTE FOR


	THE USER TABLE, YOU CAN CHANGE, ADD, REMOVE (ONLY) THE VARIABLEs/ATTRIBUTES


	ACCORDING TO THE TABLE YOU ARE MANIPULATING CONSIDERING


	THE FEATURE YOU ARE WORKING


	*WE SHOULD NOT PUT ANY QUERRIES ON THE ROUTE.PY*


'''
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