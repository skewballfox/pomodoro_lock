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
gnome environment and gnome shell extension (for toggle switch), would quit
working after a day or so. I suspect this is due to the amount of memory
allocated to the program.

July 2018
I created (read: copied and modified) a bash script that watches for lock and
unlock events, and launches this script when the screen is locked. if the
screen is unlocked during the 50 30-second intervals leading up to the end
of the 25 minute period, a flag file is created, which the script watches for.
If it exists the program exits. It is no longer recursive and has to be
launched from another program. This will hopefully prevent the program from
crashing after extended periods of Time.

August 2018
19th
I added a set of flags for setting an extended break after every fourth
pomodoro

I changed the flag files to use the /tmp directory

I changed the bash script to only create the lock flag file if the program
didn't completes successfully.

I added a running flag to prevent more than one instance running at a time.
precedence was given to the younger script, as the program should be launched
only if the screen is unlocked.

I added a timer in the bash script to reset the extended break counter if
it has been more than 15 minutes since the screen locked.

21st
I changed a few of the lines to use in the python script to use less bash
and more python builtins

September 2018
1st
I modified the monitor program to launch all scripts in a directory, I'm
going to move that to a seperate repository soon.

I fixed the issue with the counter not triggering the extended break

I implemented a rather hackish solution to detecting sleep.

7th
moved control of the extended break into the lock script itself, should simplify
things a bit, only needs to be set outside the script in cases of early lock


TODO:
priority highest to lowest

1) create a service that is constantly running in the background, or just
autostart.

2) move contents to a distro/user agnostic location

3) see if it's possible to do something other than blacking out the screen,
such as running a gif or video. mostly aesthetic, but could add to the
functionality as an actual pomodoro timer. an example would be ideas for things
to do in the time until next unlock.

5) Seperate the monitor to it's own project, and just have this
depend on that script. the reason being is that the monitor is going to be used
for quite a few scripts that revolve around screen locks and unlocks.

6) create a GUI for toggling my lock and unlock scripts, of which this is one.
 Bonus points if I can make it modular, and upload it to the AUR.


"""
import subprocess
import configparser
import time
import os
import sys
import datetime
from getpass import getuser

def log(log_contents, log_file="/tmp/lastauth.log"):
    formatted_log = '{} -- {} -- {} -- {}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S"),
    getuser(), os.path.basename(sys.argv[0]), log_contents)
    with open(log_file, 'a') as log:
        log.write(formatted_log)

def get_counter(counter_file='/tmp/pom_counter'):
    with open(counter_file, 'r') as file:
        try:
            log('reading counter from file')
            int counter=file.readline().rstrip()
        except(ValueError):
            log('counter file fail')
        return counter

def set_counter(counter,counter_file='/tmp/pom_counter'):
    log("setting counter to {}".format(counter))
    with open(counter_file, 'w') as file:
        file.write(counter)


def kill_running_pomodoro():
    """
    check to make sure this is only instance of script
    if not, kill earlier instance.

    """
    if (os.path.exists("/tmp/pom_running_flag") is True):
        log("older locker found")
        with open("/tmp/pom_running_flag") as file:
            pid = file.readline().rstrip()
        log("attempting to kill {}".format(pid))
        subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
        subprocess.call(["kill", "-9", pid])


def pomodoro():
    get = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    screens = [get[i-1] for i in range(len(get)) if get[i] == "connected"]
    subprocess.call(["touch", "/tmp/pomodoro_complete_flag"])
    counter=get_counter()

    log("starting process for locking and sleeping")
    for scr in screens:
        # lock the screen, turn the display black, and potentially activate
        # a very intensive process to further incentivise my commitment...
        subprocess.call(["xdg-screensaver", "lock"])
        subprocess.call(["xrandr", "--output", scr, "--brightness", "0"])
    log("screen locked and display blacked")
    if counter >= 4:
        log ("extended break started")
        # this will be 15 minute for 3 minute breaks
        time.sleep(sleeptime*5)
        set_counter(0)
    else:
        log("break started")
        time.sleep(sleeptime)
        set_counter(counter+1)
    log("break ended")
    for scr in screens:
        # back to "normal"
        subprocess.call(["xrandr", "--output", scr, "--brightness", "1"])
    log("screen brightened")

if __name__ == "__main__":

    log("starting")
    config = configparser.ConfigParser()
    config.sections()
    config.read('/home/daedalus/github/pomodoro_lock/config.ini')
    config.sections()

    awaketime = int(float(config.get("pomodoro_lock", "awaketime")))
    sleeptime = int(float(config.get("pomodoro_lock", "sleeptime"))*60)

    # used to tell when to make the pause longer than normal

    # check to make sure this is only instance of script
    # if not, kill earlier instance
    log("checking for running flag")
    kill_running_pomodoro()

    # write pid to file, to be used in the above verification

    pid_file = open("/tmp/pom_running_flag", "x")
    pid_file.write(("%d") % (os.getpid()))
    pid_file.close()


    previous_time = time.perf_counter()
    log("pomodoro timer started")
    for i in range(6*awaketime):
        if (os.path.exists("/tmp/pom_lock_flag") is False):
            time.sleep(10)
            if time.perf_counter() - previous_time > 12:
                log("time discrepancy noted")
                log("exiting")
                subprocess.call(["rm", "-f", "/tmp/pom_lock_flag"])
                subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
                sys.exit()
            else:
                previous_time = time.perf_counter()
        else:
            log("premature screen lock noted")
            subprocess.call(["rm", "-f", "/tmp/pom_lock_flag"])
            subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
            log("exiting")
            sys.exit()

    pomodoro(extended_break)
    log("removing running flag")
    subprocess.call(["rm", "-f", "/tmp/pom_running_flag"])
    log("exiting")
    sys.exit(0)
