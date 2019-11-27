from amsta.DBHandler import DBHandler


class FitStop:

    # --------------------
    #  Constructors
    # --------------------

    def __init__(self, stop_id, stop_location_x, stop_location_y, stop_name):
        self.stop_id = stop_id
        self.stop_location_x = stop_location_x
        self.stop_location_y = stop_location_y
        self.stop_name = stop_name

    # --------------------
    #  Getters & Setters
    # --------------------

    def get_stop_id(self):
        return self.stop_id

    def set_stop_id(self, stop_id):
        self.stop_id = stop_id

    def get_stop_location_x(self):
        return self.stop_location_x

    def set_stop_location_x(self, stop_location_x):
        self.stop_location_x = stop_location_x

    def get_stop_location_y(self):
        return self.stop_location_y

    def set_stop_location_y(self, stop_location_y):
        self.stop_location_y = stop_location_y

    def get_stop_name(self):
        return self.stop_name

    def set_stop_name(self, stop_name):
        self.stop_name = stop_name

    # --------------------
    # Functional methods
    # --------------------

    def save_stop(x, y, id):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.query_save_stop(x, y, id)
        dbh.close_connection()
        # Code to write

    # Check if user can get points
    def can_user_get_points(self, user_id):
        dbh = DBHandler()
        dbh.open_connection()
        already_has_stop_rows = dbh.did_user_get_stop_today(user_id, self.get_stop_id())
        dbh.close_connection()

        already_has_stop = already_has_stop_rows[0][0]

        print(already_has_stop)

        if already_has_stop == 1:
            return False
        else:
            return True

    def give_user_points(self, user_id):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.register_user_points(self.get_stop_id(), user_id)
        dbh.close_connection()

    def delete_stop(stop_id):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.query_delete_stop(stop_id)
        dbh.close_connection()

    def add_stop(name, location):
        dbh = DBHandler()
        dbh.open_connection()
        dbh.query_add_stop(name, location)
        dbh.close_connection()


    # --------------------
    #  Static methods
    # --------------------

    @staticmethod
    def get_stop(stop_id):
        dbh = DBHandler()
        dbh.open_connection()
        stop_rows = dbh.get_stop(stop_id)
        dbh.close_connection()

        for row in stop_rows:
            return FitStop(row[0], row[5], row[4], row[1])


    @staticmethod
    def get_stops():
        dbh = DBHandler()
        dbh.open_connection()
        all_stop = dbh.query_get_all_stops()

        stops = list()

        dbh.close_connection()
        for row in all_stop:
            stops.append(FitStop(row[0], row[5], row[4], row[1]))
        return stops