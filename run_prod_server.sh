#!/bin/bash

API_SERVER_PORT=8500
NUM_WORKER=1    #2 * num_processors + 1
NUM_THREADS_PER_WORKER=2
TIMEOUT=300


echo "-----------START API SERVER-----------"
gunicorn -b 0.0.0.0:$API_SERVER_PORT --worker-class eventlet -w $NUM_WORKER --threads $NUM_THREADS_PER_WORKER --timeout $TIMEOUT server:app