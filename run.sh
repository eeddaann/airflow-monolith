#!/bin/bash


# init airflow db
echo "init airflow db"
airflow db init
echo "airflow db created"

echo "create user"
airflow users create \
    --email foo@bar.com --firstname foo \
    --lastname bar --password airflow \
    --role Admin --username airflow

# Start the scheduler
echo "starting scheduler on background"
sh -c "airflow scheduler" &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start scheduler: $status"
  exit $status
fi
# Start the webserver
echo "starting webserver"
sh -c "airflow webserver" 
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start webserver: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  ps aux |grep scheduler |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep webserver |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done

