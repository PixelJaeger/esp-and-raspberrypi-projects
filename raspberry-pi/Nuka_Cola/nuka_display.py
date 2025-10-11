#!/usr/bin/python3
import time
import board
import adafruit_dht  # type: ignore
import tm1637  # type: ignore
from time import localtime
import argparse, numpy

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clock', action='store_true', help="shows current time")
parser.add_argument('-t', '--temperature', action='store_true', help="displays current temperature and humidity")
parser.add_argument('-b', '--both', action='store_true', help="displays time, temperature and humidity")
parser.add_argument('-d', '--debug', action='store_true', help="test")

args = parser.parse_args()

tm = tm1637.TM1637(clk=26, dio=19)                              # clk and dio need to be changes according to you pin usage
dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)    # "(board.D15) needs to be changed according to your pin usage)
tm.brightness(1)                                                # brightness settings for the LED-Display (0 = off, 7 = staring into the sun)
tm.show('    ')

def clock_time():
    t = localtime()
    tm.numbers(t.tm_hour, t.tm_min)
    time.sleep(1)
    tm.numbers(t.tm_hour, t.tm_min, False)
    time.sleep(1)
    tm.numbers(t.tm_hour, t.tm_min)
    time.sleep(1)
    tm.numbers(t.tm_hour, t.tm_min, False)
    time.sleep(1)
    tm.numbers(t.tm_hour, t.tm_min)
    time.sleep(1)
    tm.numbers(t.tm_hour, t.tm_min, False)
    #time.sleep(1)

def temp_humi():
    global temperature_c
    global humidity
    temperature_c = dhtDevice.temperature               # get temperature from sensor
    humidity = dhtDevice.humidity                       # get humidity from sensor
    tempe = str(temperature_c)                          # convert to string
    humi = str(humidity)
    tempe = tempe[:2]                                   # only use first to characters of string
    humi = humi[:2]
    tempe = tempe+'*C'                                  # append "*C" to string
    #print('temp:',tempe)                               # uncomment for console output of temperature and humidity
    #print('humi',humi)
    tm.show(tempe)                                      # show Temperature-string on LED Display
    time.sleep(3)
    tm.show('    ')                                     # clear LED Display
    tm.write([0, 0 , 0 , 116])                                     
    tm.show(humi)                                       # show Humidity-String on LED Display
    time.sleep(2)


if args.clock:
    while True:
        try:
            clock_time()
        except RuntimeError as error:
            #print(error.args[0])                   #uncomment for error messages in console
            time.sleep(1)
            continue
        except Exception as error:
            #dhtDevice.exit()                       #drops device in case of "big" errors
            #raise error                            #shows "big" errors in the console
            time.sleep(1)
            continue
        time.sleep(1)

if args.temperature:
    while True:
        try:
            temp_humi()
        except RuntimeError as error:
            #print(error.args[0])                   #uncomment for error messages in console
            time.sleep(1)
            continue
        except Exception as error:
            #dhtDevice.exit()                       #drops device in case of "big" errors
            #raise error                            #shows "big" errors in the console
            time.sleep(1)
            continue
        time.sleep(1)

if args.both:
    while True:
        try:
            clock_time()
            temp_humi()
        except RuntimeError as error:
            #print(error.args[0])                   #uncomment for error messages in console
            time.sleep(1)
            continue
        except Exception as error:
            #dhtDevice.exit()                       #drops device in case of "big" errors
            #raise error                            #shows "big" errors in the console
            time.sleep(1)
            continue
        time.sleep(1)

if args.debug:
    print('Delayvalue =', int(args.integers[0]))
