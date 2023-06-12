#!/bin/bash

function printManual(){
  echo "$(tput bold)This is Health Booking Script$(tput sgr0)"
  echo ""
  echo "$(tput bold)USAGE$(tput sgr0)"
  echo "  ./health.sh [options]"
  echo ""
  echo "$(tput bold)OPTIONS$(tput sgr0)"
  echo "  0 : use everyday"
  echo "  25: use on the 25th"
}

function book0(){
  COUNT=0
  while :
  do
    pipenv run python main.py
    let COUNT=COUNT+1
    echo attempt: $COUNT
    sleep 1200
  done
}

function book25(){
  pipenv run python main.py 25
}

ARG_1=${1}

if [ "${ARG_1}" == "0" ]; then
  book0
elif [ "${ARG_1}" == "25" ]; then
  book25
else
  printManual
fi

