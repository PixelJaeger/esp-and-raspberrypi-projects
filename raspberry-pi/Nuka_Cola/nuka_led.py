#!/usr/bin/python3
from gpiozero import PWMLED
from time import sleep
import argparse, numpy, random

led_mid = PWMLED(24)
led_up = PWMLED(22)
led_down = PWMLED(27)
led_right = PWMLED(23)
led_left = PWMLED(16)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--blink', action='store_true', help="blinking led")
parser.add_argument('-o', '--opposite', action='store_true', help="polarcoords animation")
parser.add_argument('-c', '--circle', action='store_true', help="circle animation")
parser.add_argument('-f', '--full', action='store_true', help="full lights")
parser.add_argument('-a', '--all', action='store_true', help="full animation-cycle")
parser.add_argument('-p', '--pulse', action='store_true', help="pulse animation")
parser.add_argument('integers', metavar='N', type=float, nargs='+', help='an value for the args.integers')
parser.add_argument('-t', '--test', action='store_true', help="test")
parser.add_argument('-r', '--rndpulse', action='store_true', help="random value pulses")
args = parser.parse_args()
delay = float(args.integers[0])
mid_led = 0
led_pulse_step = ['0.025','0.05','0.075','0.1']
led_pulse_start = ['0.1','0.2','0.3','0.4']
led_pulse_stop = ['1','0.9','0.8','0.7']
rnd = 0

def random_pulse():
    global rnd, pulse_step, pulse_start, pulse_stop
    rnd = random.randrange(3,10,1)
    pulse_step = float(random.choice(led_pulse_step))
    pulse_start = float(random.choice(led_pulse_start))
    pulse_stop = float(random.choice(led_pulse_stop))
    for a in range(rnd):
        for x in numpy.arange(pulse_start,pulse_stop,pulse_step):
            led_up.value = x
            led_mid.value = x
            led_down.value = x
            led_left.value = x
            led_right.value = x
            sleep(0.05)
        for x in reversed(numpy.arange(pulse_start,pulse_stop,pulse_step)):
            led_up.value = x
            led_mid.value = x
            led_down.value = x
            led_left.value = x
            led_right.value = x
            sleep(0.05)

def cycle_polar():
    global mid_led
    if mid_led == 1:
        led_mid.value = 1
    else:
        led_mid.value = 0
    led_left.value = 0
    led_right.value = 0
    led_up.value = 1
    led_down.value = 1
    sleep(delay)
    led_up.value = 0
    led_down.value = 0
    led_left.value = 1
    led_right.value = 1
    if mid_led != 1:
        mid_led = 1
    else:
        mid_led = 0
    sleep(delay)

def cycle_run():
    global mid_led
    if mid_led == 1:
        led_mid.value = 1
    else:
        led_mid.value = 0
    led_up.value = 1
    sleep(delay)
    led_up.value = 0
    led_right.value = 1
    sleep(delay)
    led_right.value = 0
    led_down.value = 1
    sleep(delay)
    led_down.value = 0
    led_left.value = 1
    sleep(delay)
    led_left.value = 0
    if mid_led != 1:
        mid_led = 1
    else:
        mid_led = 0

def cycle_full():
    led_up.value = 1
    led_down.value = 1
    led_left.value = 1
    led_right.value = 1
    led_mid.value = 1
    sleep(delay)

def cycle_off():
    led_up.value = 0
    led_down.value = 0
    led_left.value = 0
    led_right.value = 0
    led_mid.value = 0
    sleep(delay)

def cycle_pulse():
    for x in numpy.arange(0.3,1,0.025):
        led_up.value = x
        led_mid.value = x
        led_down.value = x
        led_left.value = x
        led_right.value = x
        sleep(delay/25)
    for x in reversed(numpy.arange(0.3,1,0.025)):
        led_up.value = x
        led_mid.value = x
        led_down.value = x
        led_left.value = x
        led_right.value = x
        sleep(delay/25)

if args.blink:
    while True:
        cycle_full()
        cycle_off()

if args.opposite:
    while True:
        cycle_polar()

if args.circle:
    while True:
        cycle_run()

if args.full:
    while True:
        cycle_full()

if args.pulse:
    while True:
        cycle_pulse()

if args.rndpulse:
    while True:
        random_pulse()


if args.all:
    while True:
        cycle_full()
        cycle_off()
        cycle_full()
        cycle_off()
        cycle_full()
        cycle_off()
        cycle_polar()
        cycle_polar()
        cycle_polar()
        cycle_polar()
        cycle_off()
        cycle_run()
        cycle_run()
        cycle_run()
        cycle_run()
        cycle_off()
        cycle_pulse()
        cycle_pulse()
        cycle_pulse()
        cycle_pulse()
        cycle_off()

if args.test:
    print('Delayvalue =', int(args.integers[0]))
