from dotenv import load_dotenv
from bot.logger import setup_logger
from bot.reddit_client import create_reddit_instance
from bot.searcher import search_reddit
from bot.emailer import send_email
import logging
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot'))

load_dotenv()
setup_logger()

reddit = create_reddit_instance()

to_email = input("Enter recipient email for alerts: ").strip()
if not to_email:
    to_email = os.getenv("TO_EMAIL")  # fallback if they pressed Enter

subreddits = [s.strip() for s in input(
    "Enter subreddit names (comma-separated): ").split(",") if s.strip()]
keywords = [k.strip().lower() for k in input(
    "Enter keywords separated by commas: ").split(",") if k.strip()]

send_email("Bot Started", "Your Reddit search bot is now running", to_email)

while True:
    search_reddit(reddit, subreddits, keywords, to_email, limit=90)
    logging.info("Waiting 30 seconds until next search...")
    time.sleep(30)
