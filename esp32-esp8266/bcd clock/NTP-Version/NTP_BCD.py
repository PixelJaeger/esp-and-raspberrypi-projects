import machine, neopixel, time
from machine import Pin, Signal
from ntptime import settime

########################################################################
###                    Start of adjustable values                    ###
########################################################################
# WLAN Name und Passwort
ssid = 'SSID HIER'
password = 'PASSWORT HIER'
# RGB für Stunden-LEDs  0-250
h_r=0
h_g=0
h_b=250
# RGB für Minuten LEDs  0-250
m_r=0
m_g=250
m_b=0
# RGB für Sekunden LEDs  0-250
s_r=250
s_g=0
s_b=0
# Helligkeit für weisse LEDs  0-250
pwm_bright=250
# Zeitzonen Wert CET+1 = 3600
TZ_OFFSET = 3600
########################################################################
###                     End of adjustable values                     ###
########################################################################

# Network/WLAN
try:
  import usocket as socket
except:
  import socket

import network
import esp
esp.osdebug(None)
import gc
gc.collect()

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

# adjustment for timezones
def localtime(secs=None):
  return time.localtime((secs if secs else time.time()) + TZ_OFFSET)

# get ntp-time for first time
time.sleep(1)
settime()
time.sleep(1)

# define Pin and Number of led
p = 14 # pin used for led
n = 21 # number of led
np = neopixel.NeoPixel(machine.Pin(p), n)

# pwm pin 27
pwm_leds = machine.PWM(machine.Pin(27), freq=1000)
pwm_leds.duty(pwm_bright)

# variables for led-arrays
wo = 0
zahl = 0
switch = 0

# turns led off
def clear():
    for i in range(n):
        np[i] = (0,0,0)
        np.write()

def led_on(led):
  if 0 <= led <= 6:     # led 1-6 is for seconds
    np[led] = (s_r,s_g,s_b) # make leds red
  if 7 <= led <= 13:    # led 7-13 is for minutes
    np[led] = (m_r,m_g,m_b) # make leds green
  if 14 <= led  <= 19:  # led 14-19 is for hours
    np[led] = (h_r,h_g,h_b) # make leds blue
  np.write()

# turning off leds
def led_off(led):
  np[led] = (0,0,0)
  np.write()

# I know full well that this could be done way more elegantly but it works and therefore i won't touch it.
def show_time():
  if switch == 1:
    wo = 0
  if switch == 2:
    wo = 7
  if switch == 3:
    wo = 14
  if zahl == 0:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 1:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 2:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 3:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 4:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 5:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 6:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 7:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 8:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 9:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 10:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 11:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 12:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 13:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 14:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 15:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 16:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 17:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 18:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 19:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_off(wo+5) , led_off(wo+6)
  if zahl == 20:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 21:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 22:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 23:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 24:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 25:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 26:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 27:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 28:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 29:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 30:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 31:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 32:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 33:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 34:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 35:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 36:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 37:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 38:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 39:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_on(wo+5) , led_off(wo+6)
  if zahl == 40:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 41:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 42:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 43:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 44:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 45:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 46:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 47:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 48:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 49:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_off(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 50:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 51:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 52:
    led_off(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 53:
    led_on(wo) , led_on(wo+1) , led_off(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 54:
    led_off(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 55:
    led_on(wo) , led_off(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 56:
    led_off(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 57:
    led_on(wo) , led_on(wo+1) , led_on(wo+2) , led_off(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 58:
    led_off(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)
  if zahl == 59:
    led_on(wo) , led_off(wo+1) , led_off(wo+2) , led_on(wo+3) , led_on(wo+4) , led_off(wo+5) , led_on(wo+6)


clear()
pwm_leds.duty(pwm_bright)

while True:
  ntp_hour=localtime()[3]
  ntp_min=localtime()[4]
  ntp_sec=localtime()[5]
  if ntp_hour == 3:
    if ntp_min == 30:
      if ntp_sec == 00:
        settime() # gets timedata from ntp IF it's 03:30:00

  # show seconds
  switch = 1
  now_sec = localtime()[5]
  zahl = now_sec
  show_time()

  # show minutes
  switch = 2
  now_min = localtime()[4]
  zahl = now_min
  show_time()

  # show hours
  switch = 3
  now_hour = localtime()[3]
  zahl = now_hour
  show_time()

    
