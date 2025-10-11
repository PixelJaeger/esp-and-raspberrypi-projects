import machine, neopixel, time
import dcf2rtc
from machine import Pin, Signal, RTC

# WLAN Name und Passwort
ssid = 'Nopedinger'
password = 'AlWu12031984sv.wrech'
# RGB für Stunden-LEDs
h_r=0
h_g=0
h_b=250
# RGB für Minuten LEDs
m_r=0
m_g=250
m_b=0
# RGB für Sekunden LEDs
s_r=250
s_g=0
s_b=0
# Helligkeit für weisse LEDs
pwm_bright=250
# Zeitzonen Wert CET+1 = 3600
TZ_OFFSET = 3600

rtc = RTC()

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

# to wake up dcf1 (maybe connecting to PON pin is sufficient)
pon_pin = Pin(12, Pin.OUT) #D5
#pon_pin.on()
#sleep_ms(200)
#pon_pin.off()

# dcf1
dcf = Pin(13, Pin.IN) #D6

# real time clock
rtc = RTC()

# turns led off
def clear():
    for i in range(n):
        np[i] = (0,0,0)
        np.write()

# setting color's for each segment (h,m,s) and turning individual LEDs on
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

# get DCF signal, decode it and use values as RTC
cnd = True
while cnd:
    if dcf2rtc.detectNewMinute(dcf):
        cnd = dcf2rtc.computeTime(rtc,dcf)


while True:
  hour=rtc.datetime()[4]
  minu=rtc.datetime()[5]
  secu=rtc.datetime()[6]

# gets new time from dcf @ 03:30  
  if hour == 3:
    if minu == 30:
      if secu == 00:
        cnd = True
        while cnd:
          if dcf2rtc.detectNewMinute(dcf):
            cnd = dcf2rtc.computeTime(rtc,dcf)

# maybe add check if value not changed -> don't change leds
  # show seconds
  switch = 1
  now_sec = rtc.datetime()[6]
  zahl = now_sec
  show_time()

  # show minutes
  switch = 2
  now_min = rtc.datetime()[5]
  zahl = now_min
  show_time()

  # show hours
  switch = 3
  now_hour = rtc.datetime()[4]
  zahl = now_hour
  show_time()


