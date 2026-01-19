import machine, neopixel
import time
from ntptime import settime
from machine import ADC, Pin

# uAsyncio Table
# Seconds-LEDs = await 1 second
# Minute and Hour LEDs = await 1 second (not 60 because RTC/NPT/async jitter)
# Webserver = no await value since I/O driven
# Poti/Dimmer = 20-100 milliseconds
# NTP Sync = once every 24 hours

# Beginn der einstellbaren Variabeln #
ssid = ''
password = ''
dim_tick = 0.05 # für das dimmen der LED. Nicht weniger als 0.05 weil neopixel sonst glitchen können.
# Ende der einstellbaren Variabeln # 

# "hardcodierte" Variabeln
esp_pin = 33    # Daten-Pin
led_count = 37   # Anzahl der LEDs +1
n = neopixel.NeoPixel(machine.Pin(esp_pin),led_count)

adc = ADC(Pin(32))          # bekannter, funktionierender Pin
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


def last_sunday(year, month):
    # Scan backwards from day 31
    for day in range(31, 24, -1):
        try:
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0))
            if time.localtime(t)[6] == 6:  # 6 = Sunday
                return day
        except:
            pass

def cet_offset(ts):
    y = time.localtime(ts)[0]  # year
    # DST starts last Sunday March 02:00
    dst_start = time.mktime((y, 3, last_sunday(y, 3), 2, 0, 0, 0, 0))
    # DST ends last Sunday October 03:00
    dst_end   = time.mktime((y, 10, last_sunday(y, 10), 3, 0, 0, 0, 0))

    return 7200 if dst_start <= ts < dst_end else 3600

def localtime(secs=None):
    ts = secs if secs else time.time()
    return time.localtime(ts + cet_offset(ts))

# funktionen fuer Mengenlehre-Uhrzeit zu LEDs
def set_h1(pair_index, color):
    a,b = h1_pairs[pair_index]
    n[a] = dim(color, brightness)
    n[b] = dim(color, brightness)
# set_h1(pair-number, color)

def set_h2(pair_index, color):
    a,b = h2_pairs[pair_index]
    n[a] = dim(color, brightness)
    n[b] = dim(color, brightness)
# set_h2(pair-number, color)

def set_m5(pair_index, color):
    a = m5_pairs[pair_index]
    n[a] = dim(color, brightness)
# set_m5(pair-number, color)

def set_mm(pair_index, color):
    a,b = mm_pairs[pair_index]
    n[a] = dim(color, brightness)
    n[b] = dim(color, brightness)
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


# !!!Muss VOR allen Asyncs ausgeführt werden!!!
# einmalig ausführen
# aktuelle Uhrzeit holen. Die Pause davor und danach dient zur Sicherheit
time.sleep(1)
settime()
time.sleep(1)
# !!!Muss VOR allen Asyncs ausgeführt werden!!!



# !!!Muss umgeschrieben werden!!!
# in permanenter Schleife abarbeiten
while True:
    # poti kram (BETA Version)
    raw = adc.read()
    brightness = raw / 4095

    # zeit nach mengenlehre umrechnen
    berlin()

    # Mengenlehre Uhrzeit zu den LEDs schieben
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


