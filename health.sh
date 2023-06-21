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
  PERIOD=$1
  while :
  do
    pipenv run python main.py
    let COUNT=COUNT+1
    echo ""
    echo attempt: $COUNT
    echo last attempt: `date +%r`
    echo period: `expr ${PERIOD} / 60`분 `expr ${PERIOD} % 60`초
    echo ""
    sleep ${PERIOD}
  done
}

function book25(){
  pipenv run python main.py 25
}

ARG_1=${1}
ARG_2=${2}
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

cd $SCRIPT_DIR

if [[ ${ARG_1} == 0 ]]; then
  if [[ ${ARG_2} =~ ^[0-9]+$ ]]; then
    book0 ${ARG_2}
  else
    printManual
  fi
elif [[ ${ARG_1} == 25 ]]; then
  book25
else
  printManual
fi

