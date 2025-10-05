# main_copy.py (safe: loads secrets from .env, with logging)
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import praw
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
load_dotenv()

# --- Logging setup ---
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = RotatingFileHandler(
    "bot.log", maxBytes=2000000, backupCount=5
)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[
                    file_handler, console_handler])

# ---- read secrets from environment ----
FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

if not (FROM_EMAIL and EMAIL_PASSWORD and REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET and REDDIT_USER_AGENT):
    raise SystemExit(
        "Missing one or more required environment variables. Check your .env file.")

# Ask who should receive alerts (so the recipient isn't hardcoded)
TO_EMAIL = os.getenv("TO_EMAIL") or input(
    "Enter recipient email for alerts (you): ").strip()

# --- SEND EMAIL FUNCTION ---


def send_email(subject, body, to_email=TO_EMAIL):
    from_email = FROM_EMAIL
    password = EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
            logging.info("Email alert sent")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


# --- USER INPUT FOR SUBREDDITS AND KEYWORDS ---
subreddits_input = input("Enter subreddit names (comma-separated): ")
subreddits = [s.strip() for s in subreddits_input.split(",") if s.strip()]

keywords_input = input("Enter keywords separated by commas: ")
keywords = [k.strip().lower() for k in keywords_input.split(",") if k.strip()]

# --- REDDIT CONNECTION ---
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Test the connection by printing your Reddit username
try:
    logging.info(f"Connected to Reddit as: {reddit.user.me()}")
    send_email("Bot Started", "Your Reddit search bot is now running")
except Exception as e:
    logging.error(f"Error connecting to Reddit: {e}")

seen_posts = set()  # keep track of posts already seen to avoid duplicates


def search_reddit():
    logging.info("Searching Reddit...")
    for name in subreddits:
        subreddit = reddit.subreddit(name)
        logging.info(f"Searching r/{name}")
        for post in subreddit.new(limit=10):  # limit to 10 new posts
            title = post.title.lower()
            if post.id not in seen_posts:
                if any(k in title for k in keywords):
                    logging.info(
                        f"Match found! Title: {post.title} | Link: {post.url}")
                    # Send email
                    email_subject = f"New Match: {post.title}"
                    email_body = f"{post.title}\n\nLink: {post.url}"
                    send_email(email_subject, email_body)
            seen_posts.add(post.id)
while True:
    search_reddit()
    logging.info("Waiting 10 seconds until next search...")
    time.sleep(10)
