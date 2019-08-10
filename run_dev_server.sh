#!/bin/bash

PORT=8500

echo 'Killing Server'
kill `lsof -a -t -i:$PORT`
sleep 2

echo 'Start development server'
nohup python api_server.py &> app.log &

echo 'Check if service have been started'
sleep 3
lsof -a -i:$PORT
