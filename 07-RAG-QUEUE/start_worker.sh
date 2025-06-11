#!/bin/bash

# Load environment variables from .env
export $(grep -v '^#' .env | xargs -d '\n') 

# Run the RQ worker
rq worker --with-scheduler
