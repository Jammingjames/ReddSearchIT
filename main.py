import logging
import time
import sys
import os
from dotenv import load_dotenv
from bot.logger import setup_logger
from bot.reddit_client import create_reddit_instance
from bot.searcher import search_reddit
from bot.emailer import send_email

# --- 1. CONFIGURATION SETUP (Always load .env first) ---
load_dotenv()
setup_logger()

# Remove the unnecessary path modification from the original script
# if 'bot' is a subdirectory of the script's location.

# --- 2. INITIALIZATION ---
try:
    # This will check credentials and raise an exception if they are bad
    reddit = create_reddit_instance()
except Exception:
    logging.error(
        "🔴 Fatal: Application cannot start due to Reddit connection error.")
    sys.exit(1)

# --- 3. GET USER INPUTS ---
to_email = input("Enter recipient email for alerts: ").strip()
if not to_email:
    to_email = os.getenv("TO_EMAIL")  # fallback if they pressed Enter

# Collect and clean up subreddits
subreddits = [s.strip() for s in input(
    "Enter subreddit names (comma-separated): ").split(",") if s.strip()]

# Collect and clean up keywords
keywords = [k.strip().lower() for k in input(
    "Enter keywords separated by commas: ").split(",") if k.strip()]


# --- 4. VALIDATE INPUTS AND STARTUP CHECKS ---
if not to_email:
    logging.error(
        "🔴 Fatal: Recipient email is missing. Please provide TO_EMAIL in .env or via prompt.")
    sys.exit(1)

if not subreddits:
    logging.error("🔴 Fatal: Subreddit list is empty. Exiting.")
    sys.exit(1)

if not keywords:
    logging.error("🔴 Fatal: Keyword list is empty. Exiting.")
    sys.exit(1)

# Send initial email check and confirm the bot started
if send_email("Bot Started",
              f"Your Reddit search bot is now running, searching {len(subreddits)} subreddits for {len(keywords)} keywords.",
              to_email) is False:
    logging.error("🔴 Fatal: Initial email test failed. Shutting down bot.")
    sys.exit(1)

# --- 5. MAIN LOOP ---
logging.info(f"Starting main search loop. Next run in 30 seconds.")
while True:
    try:
        search_reddit(reddit, subreddits, keywords, to_email, limit=90)
        logging.info("Waiting 30 seconds until next search...")
        time.sleep(30)
    except Exception as e:
        # Catch unexpected errors in the main loop to prevent continuous crashes
        logging.error(
            f"⚠️ An unexpected error occurred in the main loop: {e.__class__.__name__}: {e}")
        logging.info("Attempting to restart search in 60 seconds...")
        time.sleep(60)  # Wait longer after an error
