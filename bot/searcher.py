import logging
from bot.emailer import send_email

seen_posts = set()


def search_reddit(reddit, subreddits, keywords, to_email, limit=90):
    logging.info("🔎 Searching Reddit...\n")

    for name in subreddits:
        try:
            subreddit = reddit.subreddit(name)
            logging.info(f"Searching r/{name}")

            for post in subreddit.new(limit=limit):
                title = post.title.lower()

                if post.id not in seen_posts and any(k in title for k in keywords):
                    logging.info(f"✅ Match found in r/{name}: {post.title}")
                    logging.info(f"Link: {post.url}")

                    send_email(
                        f"New Match in r/{name}: {post.title}",
                        f"{post.title}\n\nLink: {post.url}",
                        to_email
                    )
                    seen_posts.add(post.id)

        except Exception as e:
            logging.warning(
                f"⚠️ Skipping subreddit '{name}' due to error: {e}")
