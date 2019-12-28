#!/usr/bin/python

##############################
#
# Pressing button MODE will cycle between the modes
# Pressing button RESET will kill the current program and retart (reset current mode)
# Pressing both buttons will kill the current program and not start a new one, to save battery life
#   in this power-save mode, pressing either button will restart the display
#
##############################

import time
import subprocess

try:
    import RPi.GPIO as gpio
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")

BUTTON_MODE  = 19  # Cycle between modes
BUTTON_RESET = 25  # Restart current mode
BUTTONS      = [BUTTON_RESET, BUTTON_MODE]
PROGRAMS     = ["demo1-snow", "demo2-hourglass", "demo3-logo"]
# FLAGS        = ["--led-rgb-sequence=rbg", "--led-brightness=100"]
FLAGS        = ["--led-brightness=20"]
MODE         = 0
PROCESS      = None


def launch():
    global PROCESS
    if PROCESS is not None:
        PROCESS.terminate()
        while PROCESS.poll() is not None:
            time.sleep(0.5)
            continue
        time.sleep(0.5)
    PROCESS = subprocess.Popen(["./" + PROGRAMS[MODE]] + FLAGS)

def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    for button in BUTTONS:
        gpio.setup(button, gpio.IN, pull_up_down=gpio.PUD_UP)
        # gpio.add_event_detect(button, gpio.FALLING, callback=handle_button, bouncetime=200)

def cleanup():
    gpio.cleanup()

def main():
    global MODE
    global PROCESS
    global PROGRAMS
    launch()
    while True:
        time.sleep(0.5)
        change_mode = gpio.input(BUTTON_MODE)
        reset_mode = gpio.input(BUTTON_RESET)

        if change_mode==0 and reset_mode==0:
            if PROCESS is not None:
                PROCESS.terminate()
                while PROCESS.poll() is not None:
                    time.sleep(0.5)
                    continue
                time.sleep(0.5)
                PROCESS = None
        elif change_mode==0:
            MODE += 1
            if MODE >= len(PROGRAMS):
                MODE = 0
            launch()
        elif reset_mode==0:
            launch()




if __name__ == '__main__':
    setup()
    try:
        main()
        cleanup()
    except KeyboardInterrupt:
        cleanup()




