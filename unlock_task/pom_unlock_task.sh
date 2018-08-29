#!/bin/bash

duration=$(cat "/tmp/seconds_file")

counter_file=/tmp/pom_counter
counter=$(cat $counter_file)

echo "$(($duration))"
echo $counter
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

echo $counter > $counter_file
