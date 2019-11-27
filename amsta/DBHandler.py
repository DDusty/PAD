import pymysql
from random import randint
from amsta.ConfigReader import ConfigReader

class DBHandler:
    # --------------------
    #  Class variables
    # --------------------

    ip_adress = ConfigReader.get_value("database_ip")
    db_name = ConfigReader.get_value("database_name")
    user_name = ConfigReader.get_value("database_user")
    password = ConfigReader.get_value("database_password")

    # --------------------
    #  Constructor
    # --------------------

    def __init__(self, ip_adress=ip_adress, db_name=db_name, user_name=user_name, password=password):
        self.ip_adress = ip_adress
        self.db_name = db_name
        self.user_name = user_name
        self.password = password
        self.database = None

    # --------------------
    #  Getters & Setters
    # --------------------

    # Gets the ip adress from the object
    def get_ip_adress(self):
        return self.ip_adress

    # Sets the ip adress of the object
    def set_ip_adress(self, ip_adress):
        self.ip_adress = ip_adress

    # Gets the database name from the object
    def get_db_name(self):
        return self.db_name

    # Sets the database name of the object
    def set_db_name(self, db_name):
        self.db_name = db_name

    # Gets the username of the object
    def get_user_name(self):
        return self.user_name

    # Sets the username of the object
    def set_user_name(self, user_name):
        self.user_name = user_name

    # Gets the password from the object
    def get_password(self):
        return self.password

    # Sets the password of the object
    def set_password(self, password):
        self.password = password

    # --------------------
    #  Functional methods
    # --------------------

    # Opens the connection with the set paramaters
        # IP adress: ip to connect to
        # Name: name of database to connect with
        # Username: username to log in with
        # Password: password of the username
    def open_connection(self):
        self.database = pymysql.connect(self.ip_adress, self.user_name, self.password, self.get_db_name())
        return True

    # Closes the database connection
    def close_connection(self):
        self.database.close()
        return True

    # Sends a Query to the connencted database and return the fetched data
        # Notice: Database connection must be opened first
    def send_query(self, query):
        cursorObject = self.database.cursor()
        cursorObject.execute(query)
        return cursorObject.fetchall()

    def send_query_insert(self, query):
        cursorObject = self.database.cursor()
        cursorObject.execute(query)
        cursorObject.execute("COMMIT")

    # --------------------
    #  Static Queries
    # --------------------

    # Query that gets a user from the given userId
    def query_get_user_from_id(self, user_id):
        print("SELECT * FROM User WHERE id_User='" + str(user_id) + "'")
        return self.send_query("SELECT * FROM User WHERE id_User='" + str(user_id) + "'")

    # Gets the number of stops the user has 'collected'
    def query_get_number_of_stop_from_id(self, user_id):
        return self.send_query("SELECT COUNT(User_id_User) "
                               "FROM User_Stop "
                               "WHERE User_id_User=" + str(user_id) + " AND DATE(datum) = CURDATE()")

    # Gets a list with the highest ranking users
        # limit : the max amount of users to return
    def query_get_highest_ranking_users(self, limit):
        query = (
                "select U.id_User, U.naam, concat_ws(\" \", U.tussenvoegsel, U.achternaam) as achternaam, "
                "sum(S.punten) as totaalPunten "
                "from User U "
                "inner join User_Stop US on U.id_User = US.User_id_User "
                "inner join Stop S on US.Stop_id_Stop = S.id_Stop "
                "group by U.id_User "
                "order by sum(S.punten) desc "
                "limit " + str(limit))
        print(query)

        return self.send_query(query)

    # Gets the amount of points a given user has
        # user_id: the id of the user to get the points from
    def query_get_points_from_user_id(self, user_id):
        return self.send_query("select sum(S.punten) as totaalPunten "
                               "from User U "
                               "inner join User_Stop US on U.id_User = US.User_id_User " 
                               "inner join Stop S on US.Stop_id_Stop = S.id_Stop "
                               "where U.id_User = " + str(user_id) + ";")

    # Gets all the fitstops
    def query_get_all_stops(self):
        return self.send_query("SELECT * FROM Stop")

    def query_get_all_users(self):
        return self.send_query("SELECT * FROM User")

    def query_delete_user(self, last_name):
        cursorObject = self.database.cursor()
        query = "DELETE FROM User WHERE achternaam = {name}" .format(name= "'" + last_name + "'")
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

    # Checks if user already recieved points from the stop
    def did_user_get_stop_today(self, user_id, stop_id):
        query = "SELECT EXISTS(SELECT * FROM User_Stop " \
                "WHERE User_id_User = " + user_id + " " \
                "AND Stop_id_Stop = " + stop_id + " " \
                "AND DATE(datum) = CURDATE()) as `exists`"
        print(query)
        return self.send_query(query)
    def query_delete_stop(self, stop_id):
        cursorObject = self.database.cursor()
        query = "DELETE FROM Stop WHERE id_Stop = {id}".format(id="'" + stop_id + "'")
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

    # Adds points to user by adding user and stop to USER_STOP table
    def register_user_points(self, stop_id, user_id):
        query = "insert into User_Stop (datum, Stop_id_Stop, User_id_User) values" \
                "(NOW(), "+stop_id+", "+user_id+")"
        print(query)
        return self.send_query_insert(query)

    def get_stop(self, stop_id):
        return self.send_query("Select * FROM Stop where id_Stop = " + str(stop_id))


    def query_save_stop(self, x, y, stop_id):
        cursorObject = self.database.cursor()
        query = "UPDATE Stop SET y = {y}, x= {x} WHERE id_Stop = {id}" .format(y=y, x=x, id="'" + stop_id + "'")
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

    def query_add_stop(self, name, location):
        cursorObject = self.database.cursor()
        query = "INSERT INTO Stop (id_Stop, naam, locatie, punten, y, x) " \
                "VALUES ({id}, {name} ,{location}, {points}, {y}, {x})"\
            .format(id="'" + str(randint(0, 123456789)) + "'", name="'" + name + "'", location= "'" + location + "'", points=10, y=0, x=0)
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

    def query_add_new_user(self, id, name, middle_name, sur_name):
        cursorObject = self.database.cursor()
        query = "insert into User (id_User, naam, tussenvoegsel, achternaam)" \
                "values ('" + id + "', '" + name + "', '" + middle_name + "', '" + sur_name + "')"
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

    def query_save_user(self, firstname, middlename, lastname):
        cursorObject = self.database.cursor()
        query = "UPDATE User SET naam = {firstname}, tussenvoegsel = {middlename}, achternaam = {lastname} WHERE id_User = {id}" \
            .format(firstname="'" + firstname + "'", middlename="'" + middlename + "'", lastname="'" + lastname + "'", id="'" + id + "'")
        cursorObject.execute(query)
        cursorObject.execute('COMMIT')

