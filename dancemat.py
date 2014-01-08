import pywinusb.hid as hid
from time import sleep
from msvcrt import kbhit

all_devices = hid.find_all_hid_devices()

dancemat = None
for device in all_devices:
  if device.product_id == 17:
    dancemat = device
    break
    
print "Found dancemat!"

dancemat.open()

def listen_to_dancemat(data):
  print_name(data)
  
  print map(bin, data[5:8])
  
def print_name(data):
  if data[7] == 32:
    print "start"
  elif data[7] == 16:
    print "select"
  elif data[7] == 4:
    print "x"
  elif data[6] == 31:
    print "left"
  elif data[7] == 1:
    print "triangle"
  elif data[6] == 47:
    print "down"
  elif data[7] == 2:
    print "square"
  elif data[5] == 255:
    print "Stay Cool!"
  elif data[6] == 79:
    print "up"
  elif data[7] == 8:
    print "circle"
  elif data[6] == 143:
    print "right"

try:  
  dancemat.set_raw_data_handler(listen_to_dancemat)

  while not kbhit() and device.is_plugged():
    sleep(0.5)
  
finally:
  dancemat.close()  