#!/usr/bin/env python3
import os
import sys
import subprocess

# Set Python path
os.environ['PYTHONPATH'] = 'backend/src'

# Change to backend directory
os.chdir('backend')

# Start the server
subprocess.run([
    sys.executable, '-m', 'uvicorn', 
    'app.main:app', 
    '--reload', 
    '--host', '0.0.0.0', 
    '--port', '8000'
])