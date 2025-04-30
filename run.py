#!/usr/bin/env python3
"""
Run script for Lead Commander

This script provides a simple way to initialize the database and run the application.
Requires Python 3.10 or higher.
"""

import os
import sys
import argparse
import subprocess
import platform

# Check Python version
if sys.version_info < (3, 10):
    print("Error: Python 3.10 or higher is required.")
    print(f"Current Python version: {platform.python_version()}")
    sys.exit(1)

def setup_environment():
    """Check if virtual environment exists, create if not"""
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            
            # Determine the pip path based on the OS
            pip_path = os.path.join('venv', 'Scripts', 'pip') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'pip')
            
            # Check if pip exists
            if not os.path.exists(pip_path):
                print(f"Pip not found at {pip_path}. Using system pip instead.")
                pip_path = 'pip'
            
            print("Installing dependencies...")
            try:
                subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Error installing dependencies with venv pip: {e}")
                print("Falling back to system pip...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        except Exception as e:
            print(f"Error setting up virtual environment: {e}")
            print("Continuing with system Python...")
    else:
        print("Virtual environment already exists.")
    
    return True

def init_database():
    """Initialize the database"""
    print("Initializing database...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Virtual environment not found. Setting up environment first...")
        setup_environment()
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    # Check if the Python executable exists
    if not os.path.exists(python_path):
        print(f"Python executable not found at {python_path}. Using system Python instead.")
        python_path = sys.executable
    
    try:
        subprocess.run([python_path, 'init_db.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error initializing database: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Falling back to system Python...")
        try:
            subprocess.run([sys.executable, 'init_db.py'], check=True)
            return True
        except Exception as e:
            print(f"Error initializing database with system Python: {e}")
            return False

def run_application():
    """Run the Flask application"""
    print("Starting Flask application...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Virtual environment not found. Setting up environment first...")
        setup_environment()
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    # Check if the Python executable exists
    if not os.path.exists(python_path):
        print(f"Python executable not found at {python_path}. Using system Python instead.")
        python_path = sys.executable
    
    try:
        subprocess.run([python_path, 'app.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Falling back to system Python...")
        try:
            subprocess.run([sys.executable, 'app.py'], check=True)
            return True
        except Exception as e:
            print(f"Error running application with system Python: {e}")
            return False

def run_tests():
    """Run the API tests"""
    print("Running API tests...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Virtual environment not found. Setting up environment first...")
        setup_environment()
    
    # Determine the python path based on the OS
    python_path = os.path.join('venv', 'Scripts', 'python') if sys.platform == 'win32' else os.path.join('venv', 'bin', 'python')
    
    # Check if the Python executable exists
    if not os.path.exists(python_path):
        print(f"Python executable not found at {python_path}. Using system Python instead.")
        python_path = sys.executable
    
    try:
        subprocess.run([python_path, 'test_api.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Falling back to system Python...")
        try:
            subprocess.run([sys.executable, 'test_api.py'], check=True)
            return True
        except Exception as e:
            print(f"Error running tests with system Python: {e}")
            return False

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
