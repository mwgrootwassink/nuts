import RPi.GPIO as GPIO
from datetime import datetime

# init
data_dir = '/data/nuts'
json_template = '{"registrationdate":"%s","value":"%s"}'
board_mode = GPIO.BOARD
board_pin = 40

#setup
GPIO.setmode(board_mode)
GPIO.setup(board_pin, GPIO.IN)
GPIO.add_event_detect(board_pin, GPIO.BOTH)

def my_callback(channel):
    value = GPIO.input(board_pin)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    fName = data_dir+'/'+current_datetime[0:4]+current_datetime[5:7]+current_datetime[8:10]+current_datetime[11:13]+current_datetime[14:16]+current_datetime[17:19]
    with open(fName, 'w') as f:
        f.write(format(json_template % (current_datetime, value)))

#main
GPIO.add_event_callback(board_pin, my_callback)
