#!/bin/bash
set -o nounset                # good practice, exit if unset variable used

lock_task_folder="/home/daedalus/github/pomodoro_lock/lock_task/"
unlock_task_folder="/home/daedalus/github/pomodoro_lock/unlock_task/"
start_task_folder="/home/daedalus/github/pomodoro_lock/start_task/"

seconds_file="/tmp/seconds_file"

pidfile=/tmp/lastaukth.pid     # lock file path
logfile=/tmp/lastauth.log     # log file path
pom_kill_flag=/tmp/pom_kill_flag


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
    for task in "$lock_task_folder"*.sh; do
      bash "$task" -H
    done
}

unlock_task()
{
  for task in "$unlock_task_folder"*.sh; do
    bash "$task" -H
  done
}

if [ -e "$pidfile" ]; then    # if lock file exists, exit
    log $0 already running...
    exit
fi


trap cleanup INT TERM EXIT    # call cleanup() if e.g. killed

log daemon started...

echo $$ > $pidfile            # create lock file with own PID inside

for task in "$start_task_folder"*.sh; do
  bash "$task" -H
done


# usually `dbus-daemon` address can be guessed (`-s` returns 1st PID found)
export $(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pidof -s dbus-daemon)/environ)

expr='type=signal,interface=org.freedesktop.ScreenSaver' # DBus watch expression here

dbus-monitor --address $DBUS_SESSION_BUS_ADDRESS "$expr" | \
    while read line; do
        case "$line" in
            *"boolean true"*)
               log session locked
               SECONDS=0
               lock_task
               ;;
            *"boolean false"*)
               log session unlocked
               echo "$SECONDS">"$seconds_file"
               unlock_task
               ;;
        esac
    done

cleanup # let's not leave orphaned lock file when the loop ends (e.g. dbus dies)
