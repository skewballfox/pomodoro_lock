#!/bin/bash
set -o nounset                # good practice, exit if unset variable used
counter=0
pomodoro_complete_flag=/tmp/pomodoro_complete_flag
pidfile=/tmp/lastaukth.pid     # lock file path
logfile=/tmp/lastauth.log     # log file path
pom_kill_flag=/tmp/pom_kill_flag
SECONDS=0

cleanup()
{                   # when cleaning up:
    rm -f $pidfile            # * remove the lock file
    trap - INT TERM EXIT      # * reset kernel signal catching
    exit                      # * stop the daemon
}

log()
{                       # simple logging format example
    echo $(date +%Y-%m-%d\ %X) -- $USER -- "$@" >> $logfile
}
lock_task()#things to be done when session is locked
{
    duration=$SECONDS
    if [ -e "$pomodoro_complete_flag" ]; then    # if lock file exists, exit
        counter=$((counter+1))
        rm -f $pomodoro_complete_flag
    else
        touch /tmp/pom_lock_flag
        counter=$((0))
    fi
}
unlock_task()
{
  if [ "$(($duration/60))" -gt "15" ]; then
      echo "$(($duration/60))"
      counter=$((0))
  elif [[ $counter == 4 ]]; then
      touch /tmp/extended_break_flag
      counter=$((0))
  fi
  if [[ ! -e $pom_kill_flag ]]; then
    /home/daedalus/github/pomodoro_lock/pomodoro_lock.py
  fi
}

if [ -e "$pidfile" ]; then    # if lock file exists, exit
    log $0 already running...
    exit
fi


trap cleanup INT TERM EXIT    # call cleanup() if e.g. killed

log daemon started...

echo $$ > $pidfile            # create lock file with own PID inside

# usually `dbus-daemon` address can be guessed (`-s` returns 1st PID found)
export $(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pidof -s dbus-daemon)/environ)

expr='type=signal,interface=org.freedesktop.ScreenSaver' # DBus watch expression here

dbus-monitor --address $DBUS_SESSION_BUS_ADDRESS "$expr" | \
    while read line; do
        case "$line" in
            *"boolean true"*)
               log session locked
               lock_task
               ;;
            *"boolean false"*)
               log session unlocked
               unlock_task
               ;;
        esac
    done

cleanup # let's not leave orphaned lock file when the loop ends (e.g. dbus dies)
