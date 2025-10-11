# in case you automated you led-script to let it run on system startup
# and want to close it, than this script is what you're looking for.
# it searches the currently running processes and looks for the name
# of your running python script and closes it's 2 processes.

# my code looks terrible, i know. was my first time needing to convert a tuple
# and i was sleep deprived when i hacked this script together...
# now i'm just too lazy to "beautify" it since it works.
# NEVER TOUCH A RUNNING SYSTEM! ;)

import signal, psutil, os
import board, neopixel
import numpy as np
from time import sleep
from os import kill
from signal import SIGKILL
from array import array

name = 'NAME_OF_YOUR_SCRIPT.PY'  # <- put the name of the running .py file here

arr = []
data = [(int(p), c) for p, c in [x.rstrip('\n').split(' ', 1) \
    for x in os.popen('ps h -eo pid:1,command')]]
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]
with open('demon.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in data))
with open("demon.txt", "r") as fp:
    for line in lines_that_contain(name, fp):
        print(line)
        arr.append(line)

linea = arr[0]
lineb = arr[1]
print(linea)
print(lineb)
numa = [int(x) for x in linea.split() if x.isdigit()] 
numa = array("i", numa)
numa = np.array(numa)
numa = np.int(numa)
numb = [int(x) for x in lineb.split() if x.isdigit()] 
numb = array("i", numb)
numb = np.array(numb)
numb = np.int(numb)

kill(numa, SIGKILL)
sleep(0.5)
kill(numb, SIGKILL)
print(' tasks closed')
sleep(0.5)

if os.path.exists("demon.txt"):
  os.remove("demon.txt")

with neopixel.NeoPixel(board.D21, 16) as pixels:
 pixels.fill((0, 0, 0))
 sleep(1)
 print(' led\'s are off...')
