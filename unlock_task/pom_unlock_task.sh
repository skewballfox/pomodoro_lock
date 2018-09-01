#!/bin/bash

duration=$(cat "/tmp/seconds_file")

counter_file=/tmp/pom_counter
counter=$(< $counter_file)

echo duration is "$(($duration))"
echo counter is $counter
if [ "$(($duration/60))" -gt "15" ]; then
    echo "longer than 15 minutes)"
    echo "Called by PID $PPID: $(< /proc/$PPID/cmdline)"
    counter=$((0))
    echo $counter > $counter_file
elif [[ $counter == 4 ]]; then
    touch /tmp/extended_break_flag
    counter=$((0))
    echo $counter > $counter_file
    echo "extended break triggered"
    echo "Called by PID $PPID: $(< /proc/$PPID/cmdline)"
fi
if [[ ! -e $pom_kill_flag ]]; then
  /home/daedalus/github/pomodoro_lock/pomodoro_lock.py
fi
