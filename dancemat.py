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
  data = ''.join(map(lambda x: bin(x)[2:].zfill(8), data[5:8]))
  print data
  print_name(data)
  
  
def print_name(data):
  if data[18] == "1":
    print "start"
  if data[19] == "1":
    print "select"
  if data[21] == "1":
    print "x"
  if data[11] == "1":
    print "left"
  if data[23] == "1":
    print "triangle"
  if data[10] == "1":
    print "down"
  if data[22] == "1":
    print "square"
  if data[0] == "1":
    print "Stay Cool!"
  if data[9] == "1":
    print "up"
  if data[20] == "1":
    print "circle"
  if data[8] == "1":
    print "right"

try:  
  dancemat.set_raw_data_handler(listen_to_dancemat)

  while not kbhit() and device.is_plugged():
    sleep(0.5)
  
finally:
  dancemat.close()  