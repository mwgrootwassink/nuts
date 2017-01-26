import RPi.GPIO as GPIO
from datetime import datetime
import shutil
import time

# init
data_dir = '/data/nuts'
data_dir_ready_to_send = data_dir+'/ready_to_send'
logfileName = data_dir+'/nuts.log'

json_template = '{"registrationdate":"%s","value":"%s"}'
board_mode = GPIO.BOARD
board_pin = 40

today = datetime.now().strftime("%Y-%m-%d")
units = 0
unit_description = "Halve liter" 

#setup
GPIO.setmode(board_mode)
GPIO.setup(board_pin, GPIO.IN)
GPIO.add_event_detect(board_pin, GPIO.BOTH)

def log(message):
    logtime_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    with open(logfileName, 'a') as logfile:
        logfile.write(logtime_datetime+" - "+message+"\n")
    logfile.close()

def my_callback(channel):
    global units
    value = GPIO.input(board_pin)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    fName = data_dir+'/'+current_datetime[0:4]+current_datetime[5:7]+current_datetime[8:10]+current_datetime[11:13]+current_datetime[14:16]+current_datetime[17:19]
    fNameReadyToSend = data_dir_ready_to_send+'/'+current_datetime[0:4]+current_datetime[5:7]+current_datetime[8:10]+current_datetime[11:13]+current_datetime[14:16]+current_datetime[17:19]
    with open(fName, 'w') as f:
        f.write(format(json_template % (current_datetime, value)))
    f.close()
    shutil.move(fName, fNameReadyToSend)
    units = units+1
    log(unit_description+" gebruikt")

#main
log("Start water-registration.py")

GPIO.add_event_callback(board_pin, my_callback)

while (1 == 1):
    # At day-change report total units used
    current_day = datetime.now().strftime("%Y-%m-%d")
    if (current_day != today):
        log("Totaal gebruik "+str(today)+": "+str(units)+" ("+unit_description+")")
        today = current_day
        units = 0
   
    #Give CPU back
    time.sleep(1)

log("End water-registration.py")
