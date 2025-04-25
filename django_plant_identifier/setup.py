#!/usr/bin/env python
"""
Setup script for the Django Plant Identifier application.
This script helps users set up the project quickly.
"""

import os
import sys
import subprocess
import shutil

def run_command(command):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def create_virtual_env():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("Virtual environment already exists.")
        return True
    
    print("Creating virtual environment...")
    return run_command("python -m venv venv")

def activate_venv():
    """Activate the virtual environment."""
    if sys.platform == "win32":
        activate_script = os.path.join("venv", "Scripts", "activate")
    else:
        activate_script = os.path.join("venv", "bin", "activate")
    
    print(f"To activate the virtual environment, run: {activate_script}")
    print("After activating, run: python setup.py --install-deps")
    return True

def install_dependencies():
    """Install project dependencies."""
    print("Installing dependencies...")
    return run_command("pip install -r requirements.txt")

def setup_database():
    """Set up the database."""
    print("Setting up database...")
    return run_command("python manage.py migrate")

def create_media_dirs():
    """Create media directories."""
    print("Creating media directories...")
    os.makedirs(os.path.join("media", "plants"), exist_ok=True)
    return True

def main():
    """Main function to run the setup."""
    if len(sys.argv) > 1 and sys.argv[1] == "--install-deps":
        # Just install dependencies
        if install_dependencies():
            setup_database()
            create_media_dirs()
            print("\nSetup completed successfully!")
            print("\nTo run the server:")
            print("python manage.py runserver")
            print("\nAccess the application at: http://127.0.0.1:8000/")
        return
    
    print("Django Plant Identifier - Setup Script")
    print("=====================================")
    
    # Create virtual environment
    if create_virtual_env():
        activate_venv()

if __name__ == "__main__":
    main()
