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
total_day_units = 0
unit_description = "Halve liter" 

#setup
GPIO.setmode(board_mode)
GPIO.setup(board_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(board_pin, GPIO.BOTH, bouncetime=500)

def log(message):
    logtime_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    with open(logfileName, 'a') as logfile:
        logfile.write(logtime_datetime+" - "+message+"\n")
    logfile.close()

def process_event():
    event_timestamp = str(datetime.now())
    event_timestamp_short = event_timestamp[0:19]
    event_timestamp_supershort = event_timestamp[0:4]+event_timestamp[5:7]+event_timestamp[8:10]+event_timestamp[11:13]+event_timestamp[14:16]+event_timestamp[17:19]
    time.sleep(1)
    value = GPIO.input(board_pin)
    print(event_timestamp+" - DO-waarde:"+str(value)+" totaal units:"+str(total_day_units))
    fName = data_dir+'/'+ event_timestamp_supershort
    fNameReadyToSend = data_dir_ready_to_send+'/'+event_timestamp_supershort
    with open(fName, 'w') as f:
        f.write(format(json_template % (event_timestamp_short, value)))
    f.close()
    shutil.move(fName, fNameReadyToSend)
    log(unit_description+" gebruikt DigitalOut-waarde:"+str(value))

#main
log("Start water-registration.py")

while (True):

    # Process detected event
    if (GPIO.event_detected(board_pin)):
        GPIO.remove_event_detect(board_pin)
        total_day_units = total_day_units+1
        process_event()
        GPIO.add_event_detect(board_pin, GPIO.BOTH, bouncetime=500)
         
    # At day-change report total_day_units
    current_day = datetime.now().strftime("%Y-%m-%d")
    if (current_day != today):
        log("Totaal gebruik "+str(today)+": "+str(total_day_units)+" ("+unit_description+")")
        today = current_day
        total_day_units = 0
   
    #Give CPU back
    time.sleep(0.10)
    

log("End water-registration.py")
