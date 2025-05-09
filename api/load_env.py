import os
from dotenv import load_dotenv

# Construct the path to the .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)