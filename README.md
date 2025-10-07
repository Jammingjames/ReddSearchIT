<p align="center">
  <img src="assets/ReddSearchIT-logo.png" alt="ReddSearchIT Logo" width="200"/>
</p>

<h3 align="center">Your intelligent guide through Reddit’s chaos</h3>

ReddSearchIT

ReddSearchIT is a Python-based Reddit content monitoring bot that searches specified subreddits for posts matching user-defined keywords. It sends real-time email alerts when matches are found. The bot can be customized for job searches, product tracking, research monitoring, and more.

Features

Searches multiple subreddits simultaneously

Filters new posts by custom keywords

Sends email notifications for matching results

Uses environment variables for secure credentials

Includes logging for debugging and long-term tracking

Project Structure
ReddSearchIT/
│
├── .env                 # Environment variables (never commit this)
├── .gitignore           # Files to exclude from Git
├── main.py              # Entry point of the bot
├── bot.log              # Log file (auto-generated)
└── README.md            # Project documentation

(After refactoring, modules like bot/emailer.py and bot/reddit_client.py will be added.)

Requirements

Python 3.8 or newer

Reddit API credentials

A Gmail account with an App Password (for sending email alerts)

Setup

Clone this repository:

git clone https://github.com/YOUR-USERNAME/ReddSearchIT.git
cd ReddSearchIT

Create a .env file in the root directory and add:

FROM_EMAIL=yourbotemail@gmail.com
EMAIL_PASSWORD=yourapppassword
REDDIT_CLIENT_ID=yourredditclientid
REDDIT_CLIENT_SECRET=yourredditclientsecret
REDDIT_USER_AGENT=youruseragent
TO_EMAIL=youremail@example.com

Install dependencies:

pip install praw python-dotenv

Run the bot:

python main.py

Logging
All activity is logged in bot.log.
This includes:
Reddit connection events
Search progress
Email alerts sent
Errors or exceptions
