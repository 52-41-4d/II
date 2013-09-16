#!/bin/bash

PROJECT_HOME=/scratch/SIGCOMM14
INPUT=$PROJECT_HOME/Input
OUTPUT=$PROJECT_HOME/Output
CODE=$PROJECT_HOME/Code

# point prerun input to full IPtoASN
usage () {
  echo "LOAD REDIS: $0 -l" 
  echo "PRERUN USAGE: $0 -p"
  echo "RUN USAGE: $0 -r"
  echo "CLEANUP USAGE: $0 -c"
}

loadDB() {
  echo "Starting Redis server in the background..."
  redis-server &
  sleep 3
  reply=`redis-cli ping`
  if [ $reply=="PONG" ]; then
      echo "Redis server started in the background - OK"
      #Add only when need to load DB - may be for the first time alone?
      #python $CODE/redisConnect.py $OUTPUT/IPtoASN.txt
  else
      echo "Please install Redis server"
  fi
}

prerun() {
  echo "Starting Redis server in the background..."
  redis-server &
  sleep 3
  reply=`redis-cli ping`
  if [ $reply=="PONG" ]; then
      echo "Redis server started in the background - OK"
  else
      echo "Please install Redis server"
  fi
}

run() { 
  echo "Did you run the tool with -p option?"
  python $CODE/ii_1.py $INPUT/dns.txt $INPUT/path.txt $OUTPUT/intermediate.json
  #python #CODE/ii_2.py
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
    l)
        loadDB
        exit 0
        ;;
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
