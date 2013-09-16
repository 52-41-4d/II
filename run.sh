#!/bin/bash

PROJECT_HOME=/scratch/SIGCOMM14
INPUT=$PROJECT_HOME/Input
OUTPUT=$PROJECT_HOME/Output
CODE=$PROJECT_HOME/Code

# point prerun input to full IPtoASN
usage () {
  echo "PRERUN USAGE: $0 -p"
  echo "RUN USAGE: $0 -r"
  echo "CLEANUP USAGE: $0 -c"
}

prerun() {
  echo "Starting Redis server in the background..."
  redis-server &
  sleep 3
  reply=`redis-cli ping`
  if [ $reply=="PONG" ]; then
      echo "Redis server started in the background - OK"
      #Add only when need to update DB
      #python $CODE/redisConnect.py $OUTPUT/IPtoASN-tmp.txt
  else
      echo "Please install Redis server"
  fi
}

run() { 
  echo "Did you run the tool with -p option?"
  python $CODE/ii.py $INPUT/dns.txt $INPUT/path.txt
}

clean() {
  echo "Clean up called..."
  REDIS_PID=`pidof redis-server`
  echo "PID of Redis is $REDIS_PID..."
  kill -9 $REDIS_PID
  echo "Redis killed - OK!"
}

while getopts ":prc" opt; do
    case $opt in
	p)
	    prerun
	    exit 0
	    ;;
	r)
	    run
	    exit 0
	    ;;
	c)
	    clean
	    exit 0
	    ;;
	\?)
	    usage
	    exit 1
	    ;;
	*)
	    usage
	    exit 1
	    ;;
    esac
done
