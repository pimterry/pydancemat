import os
import pywinusb.hid as hid
from time import sleep
from msvcrt import kbhit
import hipchat

hipchat_conn = hipchat.HipChat(token=os.environ['HipchatAuthToken'])

all_devices = hid.find_all_hid_devices()

dancemat = None
for device in all_devices:
  if device.product_id == 17:
    dancemat = device
    break
    
print "Found dancemat!"

dancemat.open()

def listen_to_dancemat(data):  
  data = ''.join(map(lambda x: bin(x)[2:].zfill(8), data[5:8]))
  print data
  print_name(data)
  
is_dancing = False
  
def print_name(data):
  global is_dancing

  if (data[0] == "1" or data[21] == "1" or data[11] == "1" or data[23] == "1" or data[10] == "1" or data[22] == "1" or data[9] == "1" or data[20] == "1" or data[8] == "1"):
    message = ""
    if data[21] == "1":
      message += "x "
    if data[11] == "1":
      message += "left "
    if data[23] == "1":
      message += "triangle "
    if data[10] == "1":
      message += "down "
    if data[22] == "1":
      message += "square "
    if data[0] == "1":
      message += "Stay Cool! "
    if data[9] == "1":
      message += "up"
    if data[20] == "1":
      message += "circle "
    if data[8] == "1":
      message += "right "
  
    if not is_dancing:
      hipchat_conn.method('rooms/message', method='POST', parameters={'room_id': 219073, 'from': 'Nick Golding', 'message': 'Is dancing: ' + message, 'color': 'random'})
    is_dancing = True
  else:
    is_dancing = False

try:  
  dancemat.set_raw_data_handler(listen_to_dancemat)

  while not kbhit() and device.is_plugged():
    sleep(0.5)
  
finally:
  dancemat.close()  