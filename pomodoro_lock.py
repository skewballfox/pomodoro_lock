#!/usr/bin/env python

import subprocess
import configparser
import time

config=configparser.ConfigParser()
config.sections()
config.read('/home/daedalus/bin/config.ini')
config.sections()

awaketime = int(float(config.get("pomodoro_lock","awaketime"))*60)
sleeptime = int(float(config.get("pomodoro_lock","sleeptime"))*60)

def pomodoro():
    get = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    screens = [get[i-1] for i in range(len(get)) if get[i] == "connected"]
    for scr in screens:
        # lock the screen, turn the display black, and potentially activate
        # a very intensive process to further incentivise my commitment...

        subprocess.call(["gnome-screensaver-command", "-l"])
        subprocess.call(["xrandr", "--output", scr, "--brightness", "0"])
        # subprocess.call([insert miner/gpu-killer start here ])

    time.sleep(sleeptime)
    for scr in screens:
        # back to "normal"
        subprocess.call(["xrandr", "--output", scr, "--brightness", "1"])
        #subprocess.call([insert miner/gpu-killer stop here])

def screensaver_check():
    lock_check="The screensaver is inactive"

    #below is the simplest way I could figure out to actually see if the screen
    #was unlocked. In the future, I may check to see if the screen locks early
    
    screensaver_process=subprocess.Popen(["gnome-screensaver-command", "-q"],
                                          stdout=subprocess.PIPE)
    screensaver_output=screensaver_process.communicate()[0].decode().strip()
    return True if screensaver_output==lock_check else False




while True:
    time.sleep(.0002)

    if screensaver_check()==True:
        
        time.sleep(awaketime)

        if screensaver_check()==True:
            pomodoro()
