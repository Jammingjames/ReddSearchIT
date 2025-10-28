import logging
import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# --- Load environment variables once at the module level (Standard Approach) ---
# This ensures the .env file is loaded before we attempt to read any variables.
load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --- Optional: Toggle emojis for production mode ---
# Default to true if not explicitly set to 'false'
SHOW_EMOJIS = os.getenv("SHOW_EMOJIS", "true").lower() == "true"
EMOJI_SEARCH = "🔎" if SHOW_EMOJIS else ""
EMOJI_LINK = "🔗" if SHOW_EMOJIS else ""


def send_email(subject, body, to_email):
    """Send both plain-text and HTML formatted email alerts for ReddSearchIT."""

    # --- Robustness check ---
    if not FROM_EMAIL or not EMAIL_PASSWORD:
        logging.error(
            "FATAL: Email credentials missing. Check your .env file.")
        return False

    # --- Create message ---
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    # --- Try to extract a link automatically using regex ---
    # This finds the first URL in the body, which is more robust than a fixed format.
    match = re.search(r'(https?://[^\s]+)', body)
    link = match.group(0) if match else ''

    # --- Plain text fallback ---
    text_body = f"{body}\n\n— Sent by ReddSearchIT {EMOJI_SEARCH}"

    # --- Clean up HTML body content ---
    # 1. Replace newlines with HTML breaks
    html_content = body.replace('\n', '<br>')

    # 2. FIX: If a link was found, remove the raw URL text (and the 'Link:' prefix)
    # from the HTML content. This prevents the link from being duplicated
    # in the body text since it will be included in the button below.
    if link:
        # Use a more aggressive cleanup on the content that appears before the link
        html_content = re.sub(r'(Link: )?' + re.escape(link),
                              '', html_content).strip('<br> ')
        # Also clean up any extra line breaks that may result from removing the link
        html_content = re.sub(r'(<br>\s*){2,}', '<br><br>', html_content)

    # --- Build HTML message ---
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto;">
        <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px;">
            <h2 style="color:#d93a00; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                {EMOJI_SEARCH} New Reddit Match Found!
            </h2>
            <p>{html_content}</p>
            
            {'' if not link else f'''
                <p style="margin-top: 25px;">
                    <a href="{link}" 
                       style="display: inline-block; padding: 10px 20px; background-color: #d93a00; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        {EMOJI_LINK} View Post on Reddit
                    </a>
                </p>
            '''}

            <hr style="border:none; border-top:1px solid #eee; margin-top: 30px;">
            <p style="font-size:0.9em; color:#555;">
              Found by <strong>ReddSearchIT</strong> — your Reddit discovery assistant 🤖
            </p>
        </div>
      </body>
    </html>
    """

    # --- Attach both plain text and HTML ---
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # --- Send email securely ---
    try:
        # Use server and port for Gmail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            logging.info(f"✅ Email sent successfully to {to_email}")
            return True

    except smtplib.SMTPAuthenticationError:
        logging.error(
            "🔴 Authentication failed — check Gmail App Password/Credentials.")
        return False
    except smtplib.SMTPRecipientsRefused:
        logging.error(
            f"🔴 Recipient address '{to_email}' was rejected by the server.")
        return False
    except Exception as e:
        logging.error(f"🔴 Failed to send email: {e.__class__.__name__}: {e}")
        return False
