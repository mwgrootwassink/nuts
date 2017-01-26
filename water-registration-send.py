from RPi import GPIO as GPIO
from datetime import datetime
import shutil
import os
import time

# init
data_dir = '/data/nuts'
data_dir_ready_to_send = data_dir+'/ready_to_send'
data_dir_processed = data_dir+'/processed'
logfileName = data_dir+'/nuts_send_service.log'

def log(message):
    logtime_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    with open(logfileName, 'a') as logfile:
        logfile.write(logtime_datetime+" - "+message+"\n")
    logfile.close()

#main
log("Start of Batch - water-registration-send.py")

while (1 == 1):
    for (root, dirs, files) in os.walk(data_dir_ready_to_send):
        for fName in files:
            fNameReadyToSend = data_dir_ready_to_send+'/'+fName
            fNameProcessed = data_dir_processed+'/'+fName
            with open (fNameReadyToSend, 'r') as f:
                json_message = f.readline()
                log(json_message)
                f.close()
            
            # send json_message to webserver

            # move file
            shutil.move(fNameReadyToSend, fNameProcessed)

    #Give CPU back
    time.sleep(1)

log("End of Batch - water-registration-send.py")
