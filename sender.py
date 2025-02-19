import openai
from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
import requests

# Instantiate the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def send_message(chat_id, text):
    """Send a message to a Telegram user."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print(f"Sent message to {chat_id}: {text}")
    print(f"Telegram response: {response.json()}")

def generate_quote(topic):
    """Generate a quote based on the selected topic using OpenAI's Chat API."""
    prompt = f"Provide an inspirational quote or fun fact about {topic}."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Ensure you have access to this model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides motivational and useful quotes and tips or cool fun facts."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.6,
        )
        quote = response.choices[0].message.content.strip()
        return quote
    except Exception as e:
        print(f"Error generating quote: {e}")
        return "Sorry, I couldn't generate a quote at this time."
