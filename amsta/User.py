from amsta.DBHandler import DBHandler
import datetime


class User:

    # --------------------
    #  Constructors
    # --------------------

    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    # --------------------
    #  Getters & Setters
    # --------------------

    def get_userid(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_all_stops(self):
        return None
        # Code to write


    # --------------------
    #  Functional methods
    # --------------------

    def register_stop(self):
        return None
        # Code to write

    def update_user(id, firstname, middlename, lastname):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.query_update_user(id, firstname, middlename, lastname)
        dbh.close_connection()

    def get_number_of_stops(self):
        dbh = DBHandler()
        dbh.open_connection()
        stops = dbh.query_get_number_of_stop_from_id(self.get_userid())
        dbh.close_connection()

        try:
            for row in stops:
                return row[0]
        except:
            return "0"

    def get_points(self):
        dbh = DBHandler()
        dbh.open_connection()
        rows = dbh.query_get_points_from_user_id(self.user_id)
        dbh.close_connection()
        for row in rows:
            return row[0]

    def delete_user(last_name):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.query_delete_user(last_name)
        dbh.close_connection()

    # --------------------
    #  Static methods
    # --------------------

    @staticmethod
    def get_user_from_id(user_id):
        dbh = DBHandler()
        dbh.open_connection()
        user = dbh.query_get_user_from_id(user_id)

        dbh.close_connection()
        # als er een user is geef die dan terug
        for row in user:
            return User(user_id, row[1], row[3])

        # mocht er geen user zijn return dan none
        return None

    @staticmethod
    def add_new_user(id):
        dbh = DBHandler()
        dbh.open_connection()

        # Voeg nieuwe user toe met de voornaam: new user en achternaam de datum en tijd van toevoeging
        dbh.query_add_new_user(id, "new user", "toegevoegd op:", datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"));

        dbh.close_connection()

    @staticmethod
    def get_all_users():
        dbh = DBHandler()
        dbh.open_connection()
        users = dbh.query_get_all_users()

        list_users = list()

        dbh.close_connection()
        for row in users:
            list_users.append(User(row[0], row[1], row[3]))

        return list_users

    @staticmethod
    def get_highest_ranking_users(limit):
        dbh = DBHandler()
        dbh.open_connection()
        sql_users = dbh.query_get_highest_ranking_users(limit)
        dbh.close_connection()

        user_list = list()

        for row in sql_users:
            user_list.append(User(row[0], row[1], row[2]))

        return user_list




