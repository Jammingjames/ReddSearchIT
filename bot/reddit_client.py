import praw
import os
import logging
from dotenv import load_dotenv

load_dotenv()


def create_reddit_instance():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    logging.info(f"Connected to Reddit as: {reddit.user.me()}")
    return reddit
