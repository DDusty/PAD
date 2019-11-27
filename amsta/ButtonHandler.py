import RPi.GPIO as GPIO
import time
import threading
import os

class Button():
    
    def __init__(self, pin, page_name_switch):
        self.pin = pin
        self.page_name_switch = page_name_switch
        self.last_state = 0
        self.current_state = 0
            

class ButtonHandler(threading.Thread):
    
    def __init__(self, buttons):
        GPIO.setmode(GPIO.BOARD)
        self.buttons = buttons
        threading.Thread.__init__(self)
        
    def run(self):
        
        for button in self.buttons:
            GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        try:
            while True:
                
                for button in self.buttons:
                    #print(str(button.pin) + " " + str(GPIO.input(button.pin)))
                    button.current_state = GPIO.input(button.pin)
                    if button.current_state != button.last_state:
                        if button.current_state == 1:
                            print("pull down " + button.page_name_switch)
                            filename = "scans/new_page.txt"
                            myfile = open(filename, 'w')
                            myfile.write(button.page_name_switch)
                            myfile.close()
                        elif button.current_state == 0:
                            print("pull up " + button.page_name_switch)
                        button.last_state = button.current_state
            
                time.sleep(.01)
    
        except Exception, e:
            print(e)
            GPIO.cleanup()
