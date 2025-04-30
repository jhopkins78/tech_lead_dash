#!/usr/bin/env python3
"""
Run script for Lead Commander

This script provides a simple way to initialize the database and run the application.
"""

import os
import sys
import argparse
import subprocess

def setup_environment():
    """Check if virtual environment exists, create if not"""
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Determine the pip path based on the OS
        pip_path = os.path.join('venv', 'Scripts', 'pip') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'pip')
        
        print("Installing dependencies...")
        subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
    
    return True

def init_database():
    """Initialize the database"""
    print("Initializing database...")
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    subprocess.run([python_path, 'init_db.py'], check=True)
    
    return True

def run_application():
    """Run the Flask application"""
    print("Starting Flask application...")
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    subprocess.run([python_path, 'app.py'], check=True)
    
    return True

def run_tests():
    """Run the API tests"""
    print("Running API tests...")
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    subprocess.run([python_path, 'test_api.py'], check=True)
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Lead Commander')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    parser.add_argument('--test', action='store_true', help='Run API tests')
    parser.add_argument('--setup', action='store_true', help='Setup the environment')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_environment()
    
    if args.init:
        init_database()
    
    if args.test:
        run_tests()
    
    if not (args.init or args.test or args.setup):
        # If no arguments are provided, run the application
        if not os.path.exists('lead_commander.db'):
            print("Database not found. Initializing...")
            init_database()
        
        run_application()

if __name__ == '__main__':
    main()
