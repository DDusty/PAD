from flask import flash, jsonify

from amsta.FitStop import FitStop

from amsta.User import User

import sys, os

class WebServer():

    # --------------------
    #  Constructors
    # --------------------

    def __init__(self, ip, port, debug=False, stop_id=1):
        self.ip = ip
        self.port = port
        self.debug = debug
        self.stop_id = stop_id

    # --------------------
    #  Getters & Setters
    # --------------------

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_port(self):
        return self.ip

    def set_port(self, port):
        self.port = port

    def get_debug(self):
        return self.debug

    def set_debug(self, debug):
        self.debug = debug

    def get_stop_id(self):
        return self.stop_id

    def set_stop_id(self, stop_id):
        self.stop_id = stop_id

    # --------------------
    # Functional maethods
    # --------------------

    def start_server(self):
        from flask import Flask, render_template, request

        app = Flask("main")

        @app.route("/highscore")
        def highscore():
            users = User.get_highest_ranking_users(10)
            return render_template('highscore.html', users=users)

        @app.route("/panel")
        def panel():
            users = User.get_all_users()
            return render_template('panel.html', users=users)

        # Delete user. url /delete/username pakt de username die je in de url meegeeft
        @app.route('/delete/<user_name>', methods=['POST'])
        def delete_user(user_name):
            User.delete_user(user_name)
            return render_template('panel.html')

        # add stop
        @app.route('/add/<stop_name>', methods=['POST'])
        def add_stop(stop_name):
            FitStop.add_stop(stop_name)
            return render_template('/admin/map')

        @app.route("/kaart")
        def kaart():
            stops = FitStop.get_stops()
            print(stops[0])
            return render_template('kaart.html', stops=stops)

        @app.route("/newpage")
        def newpage():
            file = open("scans/new_page.txt", "r")
            newpage = file.read()
            return render_template('api/get_newpage.html', page=newpage)

        @app.route("/reset_new_page")
        def reset_new_page():
            filename = "scans/new_page.txt"
            myfile = open(filename, 'w')
            myfile.write("None")
            myfile.close()
            return "success"


        @app.route("/admin/map")
        def map():
            stops = FitStop.get_stops()
            print(stops[0])
            return render_template('employer_map.html', stops=stops)

        # ajax call data. stop de data in de save_stop functie.
        @app.route('/loc_val', methods=['POST'])
        def pass_val():
            x = request.args.get('x')
            y = request.args.get('y')
            id = request.args.get('stop_id')
            FitStop.save_stop(x, y, id)
            return jsonify({'reply': 'success'})

        # ajax call data. stop data in delete_stop functie
        @app.route('/delete_stop', methods=['POST'])
        def delete_stop():
            id = request.args.get('id')
            FitStop.delete_stop(id)
            return jsonify({'reply': 'success'})

        @app.route('/add_Stop', methods=['POST'])
        def new_stop():
            if request.method == 'POST':
                name = request.form['name']
                location = request.form['location']
                FitStop.add_stop(name, location)
            else:
                print("nothing found")
            return "naam: " + name + " met de locatie: " + location + " is toegevoegd. "

        @app.route('/update_user', methods=['POST'])
        def update_user():
            if request.method == 'POST':
                firstname = request.form['firstname']
                middlename = request.form['middlename']
                lastname = request.form['lastname']
                id = request.form['id']
                User.update_user(id, firstname, middlename, lastname)
            else:
                print("nothing found")
            return "user has been updated"

        @app.route("/kies")
        def choose():
            return render_template('choose.html')

        @app.route("/getlastuser")
        def get_last_user():
            try:
                file = open("scans/" + str(self.get_stop_id()) + ".txt", "r")
                last_user_id = file.read()
                return render_template('api/get_last_user.html', last_user_id=last_user_id)
            except:
                return "No fitstop found with that id"

        @app.route("/scan")
        def home():

            # Code om parameter te fetchen
            user_id = request.args.get("user_id")
            if not user_id:
                return "Missing parameters..."

            # huidige stop opvragen
            current_stop = FitStop.get_stop(self.get_stop_id())

            # Huidige user die de paal scanned
            user = User.get_user_from_id(user_id)

            if user is None:
                User.add_new_user(user_id)
                return render_template('new_user.html')

            # TRUE als user punten verdient false als user al punten heeft gehaald bij deze stop
            able_to_get_points = current_stop.can_user_get_points(user_id)

            # Als een user nog niet de stop heeft gehad geef hem punten
            if able_to_get_points:
                current_stop.give_user_points(user.get_userid())

            # Alle stops die een user deze dag heeft gehad
            recieved_stops_today = user.get_number_of_stops()

            # Totaal aantal stops die op een dag gehaald kunnen worden
            total_amount_stops = len(FitStop.get_stops())

            # De aantal stops die een gebruiker nog kan halen vandaag
            stops_to_go = total_amount_stops - recieved_stops_today

            return render_template('home.html',
                                   user=user, recieved_stops_today=recieved_stops_today,
                                   able_to_get_points=able_to_get_points,
                                   total_amount_stops=total_amount_stops,
                                   stops_to_go=stops_to_go
                                   )

        app.run(host=self.ip, port=self.port, debug=self.debug)

    def page_exsists(self, url):
        return None

    def show_page(self):
        return None
