import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def change_profile(username, bio):
    try:
        # Update Twitter profile
        api.update_profile(name=username, description=bio)
        print(f"Updated profile: {username} - {bio}")
    except Exception as e:
        print(f"Error updating profile: {e}")

# Example usage
if __name__ == "__main__":
    new_username = "New Display Name"
    new_bio = "This is my new bio, updated by a bot!"
    change_profile(new_username, new_bio)