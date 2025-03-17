import os
import tweepy
from flask import Flask, redirect, request, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

# Ensure all environment variables are loaded
if not all([API_KEY, API_SECRET, CALLBACK_URL]):
    raise ValueError("❌ ERROR: One or more environment variables are missing!")

# Set up Flask app
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Change this to a random secure key

# Set up OAuth
auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)

@app.route("/")
def login():
    """Step 1: Redirects users to Twitter for authentication."""
    try:
        redirect_url = auth.get_authorization_url()
        session["request_token"] = auth.request_token["oauth_token"]
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"Error! Failed to get request token. {str(e)}"

@app.route("/callback")
def callback():
    """Step 2: Twitter redirects here after user authentication."""
    request_token = session.pop("request_token", None)
    auth.request_token = {
        "oauth_token": request.args.get("oauth_token"),
        "oauth_token_secret": request_token
    }

    try:
        auth.get_access_token(request.args.get("oauth_verifier"))
        api = tweepy.API(auth)

        # Change Twitter display name and bio
        new_username = "Miss Hannah's Fan"
        new_bio = "I clicked the link and now my profile is changed!"

        api.update_profile(name=new_username, description=new_bio)

        return f"✅ Success! Your profile is now: {new_username} - {new_bio}"

    except tweepy.TweepyException as e:
        return f"❌ Error updating profile: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)