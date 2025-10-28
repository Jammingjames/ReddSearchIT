import praw
import os
import logging
from dotenv import load_dotenv
from prawcore.exceptions import ResponseException, OAuthException
# Load environment variables from .env file
load_dotenv()


def create_reddit_instance():
    """
    Initializes and returns a PRAW Reddit instance after validating credentials.
    Handles potential authentication or connection errors gracefully.
    """

    # 1. Check for required environment variables first
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        logging.error(
            "🔴 Fatal: Missing one or more required environment variables (CLIENT_ID, CLIENT_SECRET, USER_AGENT).")
        raise ValueError("Missing Reddit credentials in environment.")

    try:
        # Initialize the Reddit instance
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        # 2. Test the connection by getting the user info
        # This call will raise an exception if credentials are bad or API is unreachable
        current_user = reddit.user.me()

        logging.info(f"🟢 Successfully connected to Reddit as: {current_user}")
        return reddit

    except OAuthException:
        # Handles 401 Unauthorized errors (usually wrong client_secret)
        logging.error(
            "🔴 Fatal: Authentication failed. Check your REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
        raise
    except ResponseException as e:
        # Handles other API-related errors (e.g., bad user_agent, rate limiting)
        logging.error(
            f"🔴 Fatal: Failed to connect to Reddit API (Response Error). Detail: {e}")
        raise
    except Exception as e:
        # Catch any other unexpected error
        logging.error(
            f"🔴 Fatal: An unexpected error occurred during Reddit connection. Detail: {e.__class__.__name__}: {e}")
        raise
