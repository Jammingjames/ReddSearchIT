import os
import logging
from bot.emailer import send_email  # Assuming this is in bot/emailer.py

# --- Configuration and File I/O ---
SEEN_FILE = "seen_posts.txt"
# Initialize seen_posts globally, but it's best practice to keep it managed.
# For simplicity in this structure, we keep the global load/save functions.


def load_seen_posts():
    """Load previously seen post IDs from a file."""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                # Use a generator expression for efficiency
                return set(line.strip() for line in f if line.strip())
        except Exception as e:
            logging.error(f"Failed to load seen posts file: {e}")
            return set()  # Return an empty set if loading fails
    return set()


def save_seen_posts(seen_posts):
    """Save current seen post IDs to file."""
    try:
        # Save only unique post IDs
        with open(SEEN_FILE, "w", encoding="utf-8") as f:
            for pid in seen_posts:
                f.write(f"{pid}\n")
    except Exception as e:
        logging.error(f"Failed to save seen posts file: {e}")


# Load the set once when the module is imported
seen_posts = load_seen_posts()

# --- Search Logic ---


def search_reddit(reddit, subreddits, keywords, to_email, limit=90):
    """
    Searches specified subreddits for keywords in new posts and sends email notifications.
    Updates the global seen_posts set and saves it after the search is complete.
    """
    logging.info("🔎 Starting Reddit search job...")

    # 1. Convert keywords to a set of lowercase for faster, case-insensitive checks
    # This prevents issues if 'Keywords' are mixed-case in the config.
    lower_keywords = set(k.lower() for k in keywords)

    new_matches_found = False

    for name in subreddits:
        try:
            subreddit = reddit.subreddit(name)
            logging.info(f"Searching r/{name}")

            # Iterate over the newest posts
            for post in subreddit.new(limit=limit):
                post_id = post.id
                title = post.title.lower()

                if post_id not in seen_posts:
                    # Check if any lowercase keyword is in the lowercase title
                    if any(k in title for k in lower_keywords):
                        logging.info(
                            f"✅ Match found in r/{name}: {post.title} (ID: {post_id})")

                        # Send email notification
                        send_email(
                            f"New Match in r/{name}: {post.title}",
                            f"Post Title: {post.title}\n\nLink: {post.url}",
                            to_email
                        )

                        # Add to seen_posts, but DO NOT save to file yet
                        seen_posts.add(post_id)
                        new_matches_found = True

        except Exception as e:
            # Catch exceptions related to PRAW/API access, network, etc.
            # It's good to log the error and continue to the next subreddit.
            logging.warning(
                f"⚠️ Skipping subreddit '{name}' due to error: {e.__class__.__name__}: {e}")

    # 2. Save the updated list of seen posts ONLY ONCE after all subreddits are searched
    if new_matches_found:
        save_seen_posts(seen_posts)
        logging.info(
            f"💾 Updated seen_posts.txt with {len(seen_posts)} total posts.")

    logging.info("🏁 Reddit search job finished.")
