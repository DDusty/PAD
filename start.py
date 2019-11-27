from amsta.WebServer import WebServer
from amsta.Scanner import Scanner
from amsta.ConfigReader import ConfigReader
from amsta.ButtonHandler import ButtonHandler, Button
from amsta.WaitAndExecute import WaitAndExecute
import os

# Creating two button objects
button1 = Button(ConfigReader.get_value("left_button_pin"), ConfigReader.get_value("left_button_name"))
button2 = Button(ConfigReader.get_value("right_button_pin"), ConfigReader.get_value("right_button_name"))

# Creating a button handler object and starting the object in another thread
bh = ButtonHandler([button1, button2])
bh.start()

# Creating a scanner object and starting the object in another thread
scanner = Scanner(
    ConfigReader.get_value("stopid"),
    ConfigReader.get_value("webserver_ip"),
    ConfigReader.get_value("webserver_port"),
    ConfigReader.get_value("uid_parameter_name")
)
scanner.start()

# Creating the webserver and then starting the webserver
server = WebServer(
    ConfigReader.get_value("webserver_ip"),
    ConfigReader.get_value("webserver_port"),
    ConfigReader.get_value("webserver_debug"),
    ConfigReader.get_value("stopid")
)
# starting the webserver
server.start_server()

