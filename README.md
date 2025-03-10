# Letmein
from flask import Flask, request
import tweepy
import os

app = Flask(__name__)

# Twitter API Credentials (OAuth 1.0a Required)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

@app.route("/")
def home():
    return "Click <a href='/update'>here</a> to update profile & like tweets!"

@app.route("/update")
def update_profile():
    username = "MissHannah319"
    try:
        # Retweet latest 5 tweets
        tweets = api.user_timeline(screen_name=username, count=5, tweet_mode="extended")
        for tweet in tweets:
            api.retweet(tweet.id)

        # Change profile picture
        profile_pic_path = "new_profile.jpg"
        if os.path.exists(profile_pic_path):
            api.update_profile_image(profile_pic_path)

        # Update bio & website link
        api.update_profile(description="Updated bio automatically!", url="https://example.com")

        # Like last 20 tweets from @MissHannah319
        tweets_to_like = api.user_timeline(screen_name=username, count=20, tweet_mode="extended")
        for tweet in tweets_to_like:
            api.create_favorite(tweet.id)

        return "Successfully updated profile, bio, pinned tweet, and liked tweets!"

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
