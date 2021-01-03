from cuisina_app import mysql


class chef(object):
    def __init__(self, user_id=None, username=None, password=None, email_address=None,
                     first_name=None,
                     last_name=None,
                     age = None,
                     gender = None,

                     filename = None,

                     ):

        self.user_id = user_id
        self.username = username
        self.password = password
        self.email_address = email_address

        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

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
        cursor = mysql.connection.cursor()
        sql = """SELECT r.*,i.filename, u.username FROM
                ((images AS i RIGHT JOIN recipe as r ON i.recipe_id = r.recipe_id )
                    JOIN user AS u ON u.user_id = r.user_id)
                        WHERE r.user_id = {} ORDER BY r.time_date""".format(self.user_id)

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
        sql = """UPDATE profile SET first_name = '{}', last_name = '{}', age = '{}', gender = '{}' 
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

