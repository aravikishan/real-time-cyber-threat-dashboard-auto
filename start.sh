#!/bin/bash
set -e
echo "Starting Real-Time Cyber Threat Dashboard..."
uvicorn app:app --host 0.0.0.0 --port 9027 --workers 1
