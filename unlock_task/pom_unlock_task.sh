#!/bin/bash

pom_kill_flag=/tmp/pom_kill_flag

duration=$(cat "/tmp/seconds_file")

counter_file=/tmp/pom_counter
counter=$(< $counter_file)

touch /tmp/verify_unlock_running_flag

if [ "$(($duration/60))" -gt "15" ]; then
    echo "period since last screen lock longer than 15 minutes"

    counter=$((0))
    echo $counter > $counter_file
elif [[ $counter == 4 ]]; then
    touch /tmp/extended_break_flag
    counter=$((0))
    echo $counter > $counter_file
    echo "extended break triggered"

fi
if [[ ! -e $pom_kill_flag ]]; then
  echo "pomodoro_lock launched"
  exec /home/daedalus/github/pomodoro_lock/pomodoro_lock.py
fi
