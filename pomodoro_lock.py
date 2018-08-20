#!/usr/bin/env python3
"""
Pomodoro_lock

Author: Joshua Ferguson

Purpose: to lock the screen after a decided upon length of time (currently 25
minutes), and prevent the user from logging in for a decided length of time
(currently 3 minutes).

ChangeLog:
2017
Created Script, was set to loop infinitely, didn't have the ability to know
if the session had locked in the time of the script running. depended on
gnome environment and gnome shell extension (for toggle switch), would quit working
after a day or so. I suspect this is due to the amount of memory allocated to the
program.

July 2018
I created (read: copied and modified) a bash script that watches for lock and
unlock events, and launches this script when the screen is locked. if the screen
is unlocked during the 50 30-second intervals leading up to the end of the 25
minute period, a flag file is created, which the script watches for. If it exists
the program exits. It is no longer recursive and has to be launched from another
program. This will hopefully prevent the program from crashing after extended
periods of Time.

August 2018
I added a set of flags for setting an extended break after every fourth pomodoro

TODO:
priority highest to lowest

1) set the program to use the /tmp directory for all flags. this gets us closer
to the end goal of having a user agnostic process.

2) create a kill script, or some way of stopping the pomodoro process.

3) move or copy contents to user bin folder or preferably a user agnostic
location

4) create a set of flags that will reset the counter if the screen is unlocked
within a certain time frame of the pomodoro ending. this prevents a long pomodoro
being triggered uneccessarily after some time away from the computer.

5) create a service that is constantly running in the background, or just
autostart.

6) see if it's possible to do something other than blacking out the screen,
such as running a gif or video. mostly aesthetic, but could add to the
functionality as an actual pomodoro timer.

7) create a user script log file to document all my user scripts, or which this
is just one.

8)create a GUI for toggling my lock and unlock scripts, of which this is one.
Bonus points if I can make it modular, and upload it to the AUR.


"""
import subprocess
import configparser
import time
import os


config=configparser.ConfigParser()
config.sections()
config.read('config.ini')
config.sections()

awaketime = int(float(config.get("pomodoro_lock","awaketime")))
sleeptime = int(float(config.get("pomodoro_lock","sleeptime"))*60)

extended_break=False #used to tell when to make the pause longer than normal

def pomodoro(extended_break=False):
    get = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    screens = [get[i-1] for i in range(len(get)) if get[i] == "connected"]
    subprocess.call(["touch","pomodoro_complete_flag"])
    for scr in screens:
        # lock the screen, turn the display black, and potentially activate
        # a very intensive process to further incentivise my commitment...
        subprocess.call(["xdg-screensaver", "lock"])
        subprocess.call(["xrandr", "--output", scr, "--brightness", "0"])


    if extended_break is False:
        time.sleep(sleeptime)
    else:
        time.sleep(sleeptime*5)#this will be 15 minute for 3 minute breaks
    for scr in screens:
        # back to "normal"
        subprocess.call(["xrandr", "--output", scr, "--brightness", "1"])






if (os.path.exists("./flag_file")==True):
    subprocess.call(["rm", "./flag_file"])
if (os.path.exists("./long_flag")==True):
    extended_break=True
    subprocess.call(["rm", "./long_flag"])
for i in range(2*awaketime):
    if (os.path.exists("./flag_file")==False):
        time.sleep(30)
    else:
        sys.exit()
pomodoro();
