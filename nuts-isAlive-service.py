import smtplib
import os
from datetime import datetime
import socket

# init
data_dir = '/data/nuts'
logfileName = data_dir+'/isAlive_service.log'
processoOutput = os.popen("ps -Af").read()
wrsCount = processoOutput.count('water-registration-send.py')
emailMessage = """From: Raspberry PI raspberry@grootwassink.nl
To: raspberry@grootwassink.nl
Subject: git-project/nuts/water-registration-send.py is not running!

water-registration-send.py op Raspberry Pi voor NUTS-project is not running 

This mail is send by an automated process on Raspberry Pi
"""

def log(message):
    logtime_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    with open(logfileName, 'a') as logfile:
        logfile.write(logtime_datetime+" - "+message+"\n")
    logfile.close()

try:
    smtpObj = smtplib.SMTP('smtp.grootwassink.nl')
    if (wrsCount == 0):
        log("isAlive-service: Process water-registration-send is not running well")
        smtpObj.sendmail('Maarten Groot Wassink','raspberrypi@grootwassink.nl', emailMessage)
        os.popen("python3 /home/pi/git-projects/nuts/water-registration-send.py &")
except SMTPException:
    log("isAlive-service: Unable to send email")

wrsCount = processoOutput.count('water-registration.py')
emailMessage = """From: Raspberry PI raspberry@grootwassink.nl
To: raspberry@grootwassink.nl
Subject: git-project/nuts/water-registration.py is not running!

water-registration.py op Raspberry Pi voor NUTS-project is not running 

This mail is send by an automated process on Raspberry Pi
"""

try:
    smtpObj = smtplib.SMTP('smtp.grootwassink.nl')
    if (wrsCount == 0):
        log("isAlive-service: Process water-registration is not running well")
        smtpObj.sendmail('Maarten Groot Wassink','raspberrypi@grootwassink.nl', emailMessage)
        os.popen("python3 /home/pi/git-projects/nuts/water-registration.py &")
except SMTPException:
    log("isAlive-service: Unable to send email")

