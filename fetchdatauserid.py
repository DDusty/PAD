#!/usr/bin/env python

import MySQLdb
import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()
##rfid lees gedoe
while True:
    #print("je kan nu scannen")

    try:
        userid, text = reader.read()
	#print (userid)
    finally:
        #print("gescant")
##database connectie
    db = MySQLdb.connect(host="145.92.203.241",
		db="zbarane",
		user="barane",
		passwd="ElEwc3cbC96Z2q")
    curs=db.cursor()
    #print("database connected")
##waar alle data word gepakt van server met sql
    curs.execute("SELECT * FROM User WHERE id_User=%s",(userid,))

    try:
        gebruikersdata = curs.fetchall()
	#print "data pakken is gelukt"
        for row in gebruikersdata:
            gebruikersvn = row[1]
            gebruikerstv = row[2]
            gebruikersan = row[3]
            
    except:
	#print "niet gelukt"
	db.rollback
	
    #print (gebruikersvn)



