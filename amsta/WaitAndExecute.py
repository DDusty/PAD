import time
import threading
import os


class WaitAndExecute(threading.Thread):
    
    def __init__(self, seconds, command):
        self.seconds = seconds
        self.command = command
        threading.Thread.__init__(self)
        
    def run(self):
        time.sleep(self.seconds)
        os.system(self.command)