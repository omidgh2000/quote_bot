# app.py

from flask import Flask, request
import requests
import json
import schedule
import time
import threading
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, DAILY_QUOTE_TIME, TOPICS_DATA
from sender import send_message, generate_quote

app = Flask(__name__)

# Dictionary to keep track of user states
user_states = {}

# Function to send daily quote
def send_daily_quote():
    """Send a daily quote based on the day's topic."""
    day_of_week = datetime.now().strftime('%A')
    if day_of_week in TOPICS_DATA:
        topic = TOPICS_DATA[day_of_week]
        quote = generate_quote(topic)
        # Replace 'YOUR_CHAT_ID' with the chat ID where you want to send the daily quote
        send_message('YOUR_CHAT_ID', f"Today's topic is '{topic}'. Here's your quote:\n\n{quote}")

# Schedule the daily quote
schedule.every().day.at(DAILY_QUOTE_TIME).do(send_daily_quote)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def receive_update():
    """Receives updates from Telegram and processes commands."""
    update = request.json
    print(f"Received update: {update}")

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        # Check if user is in the middle of a topic selection
        if chat_id in user_states and user_states[chat_id] == "awaiting_topic":
            if text in TOPICS_DATA.values():
                quote = generate_quote(text)
                send_message(chat_id, quote)
                user_states.pop(chat_id)  # Reset user state
            else:
                send_message(chat_id, "Please choose a valid topic from the list.")
        elif text == "/quote":
            # Send list of topics
            topics_list = "\n".join(TOPICS_DATA.values())
            message = f"Choose a topic:\n{topics_list}"
            send_message(chat_id, message)
            user_states[chat_id] = "awaiting_topic"
        else:
            send_message(chat_id, "Unknown command. Please use /quote to get started.")

    return 'OK', 200

@app.route('/', methods=['GET'])
def index():
    return 'Telegram Bot is running.', 200

if __name__ == '__main__':
    print("Starting Telegram Bot Server...")
    app.run(host='0.0.0.0', port=5000)
