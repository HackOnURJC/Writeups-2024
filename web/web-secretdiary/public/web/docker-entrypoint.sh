#!/bin/bash
set -e

python3 worker.py &
python3 app.py
