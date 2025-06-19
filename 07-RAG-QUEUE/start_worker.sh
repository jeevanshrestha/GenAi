#!/bin/bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# Load environment variables from .env
export $(grep -v '^#' .env | xargs -d '\n') 

# Run the RQ worker
rq worker --with-scheduler
