import machine, neopixel
import time
from ntptime import settime
from machine import ADC, Pin

# Beginn der einstellbaren Variabeln #
ssid = ''
password = ''
#poti_div = 16   # Divisor für Poti-Wert. Poti_max war bei 4096. Also 4096 / 16 = 255 # "richtige" version ist anscheinend Raw-Wert / 4097... diese Zeile ist also sinnlos
dim_tick = 0.05 # für das dimmen der LED. Nicht weniger als 0.05 weil neopixel sonst glitchen können.
TZ_OFFSET = 3600 # Zeizzonen BS
# Ende der einstellbaren Variabeln # 


# "hardcodierte" Variabeln
esp_pin = 13    # Daten-Pin
led_count = 37   # Anzahl der LEDs +1
n = neopixel.NeoPixel(machine.Pin(esp_pin),led_count)

adc = ADC(Pin(1))          # bekannter, funktionierender Pin
adc.atten(ADC.ATTN_11DB)    # volle 0–3.3V
adc.width(ADC.WIDTH_12BIT)


# Farben der LEDs
aus = 0,0,0
red = 255,0,0
yel = 255,180,0


# LED Paare
h1_pairs = [(2,3),(4,5),(6,7),(8,9)]
h2_pairs = [(10,11),(12,13),(14,15),(16,17)]
m5_pairs = [(18),(19),(20),(21),(22),(23),(24),(25),(26),(27),(28)]
mm_pairs = [(29,30),(31,32),(33,34),(35,36)]


# Netzwerk/WLAN anwerfen
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

# funktionen fuer Mengenlehre-Uhrzeit zu LEDs
def set_h1(pair_index, color):
    a,b = h1_pairs[pair_index]
#    print(a,color)
#    print(b,color)
    n[a] = color
    n[b] = color
# set_h1(pair-number, color)

def set_h2(pair_index, color):
    a,b = h2_pairs[pair_index]
#    print(a,color)
#    print(b,color)
    n[a] = color
    n[b] = color
# set_h2(pair-number, color)

def set_m5(pair_index, color):
    a = m5_pairs[pair_index]
#    print(a,color)
    n[a] = color
# set_m5(pair-number, color)

def set_mm(pair_index, color):
    a,b = mm_pairs[pair_index]
#    print(a,color)
#    print(b,color)
    n[a] = color
    n[b] = color
# set_mm(pair-number, color)

# Dimmer-Funktion
def dim(color, brightness):
    r, g, b = color
    return (
        int(r * brightness),
        int(g * brightness),
        int(b * brightness)
    )


#umrechnen von normaler Uhrzeit nach mengen-unhrzeit
def berlin():
    global h1
    global h2
    global mm
    global m5
    now = localtime()
    for x in range(4):
        h1, h2 = divmod(now[3], 5)
        mm = now[4] % 5
    for x in range(11):
        m5 = now[4] // 5
    print(h1,h2,m5,mm) #debug


#einmalig ausführen
# aktuelle Uhrzeit holen. Die Pause davor und danach dient zur Sicherheit
time.sleep(1)
settime()
time.sleep(1)


# in permanenter Schleife abarbeiten
while True:
    # poti kram (BETA Version)
    raw = adc.read()
    brightness = raw / 4095

    # zeit nach mengenlehre umrechnen
    berlin()

    # Mengenlehre Uhrzeit zu den LEDs schieben
    # kurze version
    # h1 and h2
    for i in range(4):
        set_h1(i, red if i < h1 else aus)
        set_h2(i, red if i < h2 else aus)
    # mm
    for i in range(4):
        set_mm(i, yel if i < mm else aus)
    
    # m5
    m5_pattern = [yel, yel, red, yel, yel, red, yel, yel, red, yel, yel]
    for i in range(11):
        set_m5(i, m5_pattern[i] if i < m5 else aus)

    # sekunden
    if localtime()[5] % 2 == 0:
        n[0]=aus
        n[1]=aus
    else:
        n[0]=dim(yel, brightness)
        n[1]=dim(yel, brightness)
    
    # alle geschriebene LED-Buffer anzeigen
    n.write()

    # jeden Tag um 03:30:00 neue NTP-Zeit greifen
    ntp_hour=localtime()[3]
    ntp_min=localtime()[4]
    ntp_sec=localtime()[5]
    if ntp_hour == 3:
        if ntp_min == 30:
            if ntp_sec == 00:
                settime()
                print('ntp get interval met')
    
    time.sleep(dim_tick)






'''
# Mengenlehre Uhrzeit zu den LEDs schieben
# lange version, falls die kurze nicht funktioniert
if h1==0:
    set_h1(0, aus)
    set_h1(1, aus)
    set_h1(2, aus)
    set_h1(3, aus)
if h1==1:
    set_h1(0, red)
    set_h1(1, aus)
    set_h1(2, aus)
    set_h1(3, aus)
if h1==2:
    set_h1(0, red)
    set_h1(1, red)
    set_h1(2, aus)
    set_h1(3, aus)
if h1==3:
    set_h1(0, red)
    set_h1(1, red)
    set_h1(2, red)
    set_h1(3, aus)
if h1==4:
    set_h1(0, red)
    set_h1(1, red)
    set_h1(2, red)
    set_h1(3, red)


if h2==0:
    set_h2(0, aus)
    set_h2(1, aus)
    set_h2(2, aus)
    set_h2(3, aus)
if h2==1:
    set_h2(0, red)
    set_h2(1, aus)
    set_h2(2, aus)
    set_h2(3, aus)
if h2==2:
    set_h2(0, red)
    set_h2(1, red)
    set_h2(2, aus)
    set_h2(3, aus)
if h2==3:
    set_h2(0, red)
    set_h2(1, red)
    set_h2(2, red)
    set_h2(3, aus)
if h2==4:
    set_h2(0, red)
    set_h2(1, red)
    set_h2(2, red)
    set_h2(3, red)


if m5==0:
    set_m5(0, aus)
    set_m5(1, aus)
    set_m5(2, aus)
    set_m5(3, aus)
    set_m5(4, aus)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==1:
    set_m5(0, yel)
    set_m5(1, aus)
    set_m5(2, aus)
    set_m5(3, aus)
    set_m5(4, aus)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==2:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, aus)
    set_m5(3, aus)
    set_m5(4, aus)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==3:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, aus)
    set_m5(4, aus)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==4:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, aus)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==5:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, aus)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==6:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, aus)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==7:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, yel)
    set_m5(7, aus)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==8:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, yel)
    set_m5(7, yel)
    set_m5(8, aus)
    set_m5(9, aus)
    set_m5(10, aus)
if m5==9:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, yel)
    set_m5(7, yel)
    set_m5(8, red)
    set_m5(9, aus)
    set_m5(10, aus)
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, yel)
    set_m5(7, yel)
    set_m5(8, red)
    set_m5(9, yel)
    set_m5(10, yel)
if m5==11:
    set_m5(0, yel)
    set_m5(1, yel)
    set_m5(2, red)
    set_m5(3, yel)
    set_m5(4, yel)
    set_m5(5, red)
    set_m5(6, yel)
    set_m5(7, yel)
    set_m5(8, red)
    set_m5(9, yel)
    set_m5(10, yel)


if mm==0:
    set_mm(0, aus)
    set_mm(1, aus)
    set_mm(2, aus)
    set_mm(3, aus)
if mm==1:
    set_mm(0, yel)
    set_mm(1, aus)
    set_mm(2, aus)
    set_mm(3, aus)
if mm==2:
    set_mm(0, yel)
    set_mm(1, yel)
    set_mm(2, aus)
    set_mm(3, aus)
if mm==3:
    set_mm(0, yel)
    set_mm(1, yel)
    set_mm(2, yel)
    set_mm(3, aus)
if mm==4:
    set_mm(0, yel)
    set_mm(1, yel)
    set_mm(2, yel)
    set_mm(3, yel)
'''
