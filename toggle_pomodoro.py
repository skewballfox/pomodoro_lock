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
from pomodoro_lock import kill_running_pomodoro

if (len(sys.argv)>1):
    if (sys.argv[1].lower()) == "on":
        if (os.path.exists("/tmp/pom_kill_flag")==True):
            subprocess.call(["rm", "-f", "/tmp/pom_kill_flag"])
            #add line to launch script if not already running
        else:
            print("Pomodoro lock was already running normally")
            sys.exit(0)
    elif (sys.argv[1].lower()) == "off":
        if (os.path.exists("/tmp/pom_kill_flag")==False):
            open("/tmp/pom_kill_flag", "x").close()
            kill_running_pomodoro()
        else:
            print("Pomodoro lock was already halted")
    else:
        print(sys.argv[1].lower())
        sys.exit("CURRENTLY UNSUPPORTED ARGUMENT")
