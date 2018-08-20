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
19th
I added a set of flags for setting an extended break after every fourth pomodoro

I changed the flag files to use the /tmp directory

I changed the bash script to only create the lock flag file if the program didn't
completes successfully.

I added a running flag to prevent more than one instance running at a time.
precedence was given to the younger script, as the program should be launched
only if the screen is unlocked.

I added a timer in the bash script to reset the extended break counter if
it has been more than 15 minutes since the screen locked.

TODO:
priority highest to lowest

1)rework code to remove some of the unnecessary subprocess calls. This will
improve security and make it slightly more linux agnostic.

1) create a kill script, or some way of stopping the pomodoro process.

2) create a service that is constantly running in the background, or just
autostart.

3) move or copy contents to user bin folder or preferably a user agnostic
location

4) see if it's possible to do something other than blacking out the screen,
such as running a gif or video. mostly aesthetic, but could add to the
functionality as an actual pomodoro timer.

5) create a user script log file to document all my user scripts, or which this
is just one.

6)create a GUI for toggling my lock and unlock scripts, of which this is one.
Bonus points if I can make it modular, and upload it to the AUR.


"""
import subprocess
import configparser
import time
import os
import sys

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




#commented out following code because I don't know if I should keep it
#mainly trying to prevent interference of 2 seperate scripts

if (os.path.exists("/tmp/pom_running_flag")==True):
    subprocess.call(["kill", "-9", "$(cat /tmp/pom_running_flag)"])

subprocess.call(["touch", "/tmp/pom_running_flag"])
subprocess.call(["echo", "$$", ">", "/tmp/pom_running_flag"])

if (os.path.exists("/tmp/extended_break_flag")==True):
    extended_break=True
    subprocess.call(["rm", "-f", "/tmp/extended_break_flag"])
for i in range(6*awaketime):
    if (os.path.exists("/tmp/pom_lock_flag")==False):
        time.sleep(10)
    else:
        subprocess.call(["rm", "-f", "/tmp/pom_lock_flag"])
        subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
        sys.exit()
pomodoro();
subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
sys.exit(0)
