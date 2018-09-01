#!/bin/bash
pomodoro_complete_flag=/tmp/pomodoro_complete_flag

counter_file=/tmp/pom_counter
counter=$(cat $counter_file)

if [ -e "$pomodoro_complete_flag" ]; then    # if lock file exists, exit
    counter=$((counter+1))
    echo "pom was completed"
    echo "Called by PID $PPID: $(< /proc/$PPID/cmdline)"
    echo $counter > $counter_file
    rm -f $pomodoro_complete_flag
else
    touch /tmp/pom_lock_flag
    counter=$((0))
    echo "Pom was not completed"
    echo "Called by PID $PPID: $(< /proc/$PPID/cmdline)"
    echo $counter > $counter_file
fi
