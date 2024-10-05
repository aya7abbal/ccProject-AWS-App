import sys
import os

# Set the working directory to the Flask app directory
os.chdir('/home/ubuntu/flaskapp')

# Add the project directory to the sys.path
sys.path.insert(0, "/home/ubuntu/flaskapp")

# Specify the path to your virtual environment
virtual_env = "/home/ubuntu/flaskapp/venv"

# Set environment variables for the virtual environment
os.environ["VIRTUAL_ENV"] = virtual_env
os.environ["PATH"] = virtual_env + "/bin:" + os.environ["PATH"]

# Include the virtual environment's Python packages
sys.path.insert(1, virtual_env + "/lib/python3.12/site-packages")

# Import the Flask application
from flaskapp import app as application