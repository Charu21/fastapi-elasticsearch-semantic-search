#!/bin/bash
# Usage: ./wait-for-it.sh host:port [-t timeout]

TIMEOUT=15
HOST=""
PORT=""

if [[ "$1" != "" ]]; then
    IFS=':' read HOST PORT <<< "$1"
fi

while getopts "t:" arg; do
  case $arg in
    t)
      TIMEOUT="${OPTARG}"
      ;;
  esac
done

echo "Waiting for $HOST:$PORT to be available..."

for i in $(seq $TIMEOUT); do
  nc -z $HOST $PORT
  result=$?
  if [ $result -eq 0 ]; then
    echo "$HOST:$PORT is available after $i seconds"
    exit 0
  fi
  sleep 1
done

echo "Timed out waiting for $HOST:$PORT"
exit 1
