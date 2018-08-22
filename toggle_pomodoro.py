#!/usr/bin/env python3
"""
toggle_pomodoro

Author: Joshua Ferguson

purpose: to toggle the pomodoro script on and off, in case I'm either in class
doing something time sensitive
ChangeLog:

August 2018
21st
Created initial version, right now just toggles on and off

TODO:
priority highest to lowest

1)implement some way of setting a timer, like off for a specified time.

2)implement another script to set to turn off pomodor automatically at specified
times(such as class)

3)implement arg parser and try to make behavior more like a traditional command
line tool

4) implement logging

"""
import sys
import os
import subprocess
import time
from pomodoro_lock import kill_running_pomodoro

def toggle_on():
    if (os.path.exists("/tmp/pom_kill_flag")==True):
        subprocess.call(["rm", "-f", "/tmp/pom_kill_flag"])
        #I want to implement some way to indepedently lauch below
    else:
        print("kill flag didn't exist")

    if (os.path.exists("/tmp/pom_running_flag")==False):
        subprocess.Popen("/home/daedalus/github/pomodoro_lock/pomodoro_lock.py")
    else:
        print("pomodoro lock was already running")

def toggle_off():
    if (os.path.exists("/tmp/pom_kill_flag")==False):
        open("/tmp/pom_kill_flag", "x").close()
    else:
        print("kill flag already exists")

    if (os.path.exists("/tmp/pom_running_flag")==True):
        kill_running_pomodoro()
    else:
        ("Pomodoro lock was already halted")

if (len(sys.argv)>1):
    if (sys.argv[1].lower()) == "on":
        toggle_on();

        sys.exit(0)

    elif (sys.argv[1].lower()) == "off":

        toggle_off();

        sys.exit(0)
    elif (sys.argv[1].lower() == "sleep"):
        toggle_off();
        try:
            time.sleep(int(sys.arv[2])*60)
        except ValueError:
            sys.exit("SLEEP MUST BE FOLLOWED BY NUMBER");
    else:
        print(sys.argv[1].lower())
        sys.exit("CURRENTLY UNSUPPORTED ARGUMENT")
