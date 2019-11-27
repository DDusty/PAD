import threading
import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522


class Scanner(threading.Thread):

    def __init__(self, stop_id, url, port, uid_parameter_name):
        self.stop_id = stop_id
        self.url = url
        self.port = port
        self.uid_parameter_name = uid_parameter_name
        threading.Thread.__init__(self)

    def run(self):
        reader = SimpleMFRC522()

        while True:
            try:
                id, text = reader.read()
                print(id)
                self.new_user_id(id)
                print(text)
                time.sleep(2)
            finally:
                print("no cleanup")
                # GPIO.cleanup()

    # Writes the new page in the newpage file so it can be fetched
    def new_user_id(self, user_id):
        filename = "scans/new_page.txt"
        myfile = open(filename, 'w')
        myfile.write("scan?" + self.uid_parameter_name + "=" + str(user_id))
        myfile.close()

