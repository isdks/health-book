#!/bin/bash

COUNT=0
while :
do
    pipenv run python main.py
    let COUNT=COUNT+1
    echo attempt: $COUNT
    sleep 1200
done
