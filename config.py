import os
from dotenv import load_dotenv
import json
    
# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Time to send daily quotes (24-hour format, e.g., '09:00' for 9 AM)
DAILY_QUOTE_TIME = '09:00'

# Construct the correct path to topics.json
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this file
topics_file_path = os.path.join(base_dir, 'data', 'topics.json')  # Set the path to the JSON file

# Load topics from JSON file
try:
    with open(topics_file_path, 'r') as file:
        TOPICS_DATA = json.load(file)
    print(f"Loaded topics: {TOPICS_DATA}")
except FileNotFoundError:
    print(f"Error: topics.json not found at {topics_file_path}")
    TOPICS_DATA = {}  # Default to an empty dictionary
