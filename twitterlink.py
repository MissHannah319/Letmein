import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

# Fetch environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

# Debugging: Print the environment variables to check if they are loaded
print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)
print("ACCESS_TOKEN:", ACCESS_TOKEN)
print("ACCESS_TOKEN_SECRET:", ACCESS_TOKEN_SECRET)
print("CALLBACK_URL:", CALLBACK_URL)

# Ensure all environment variables are loaded
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CALLBACK_URL]):
    raise ValueError("❌ ERROR: One or more environment variables are missing!")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET, CALLBACK_URL)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to change Twitter display name and bio
def change_profile():
    try:
        new_username = "Miss Hannah's Fan"
        new_bio = "I clicked the link and now my profile is changed!"
        
        # Update Twitter profile
        api.update_profile(name=new_username, description=new_bio)
        print(f"✅ Success! Profile updated to: {new_username} - {new_bio}")
    
    except tweepy.TweepyException as e:
        print(f"❌ Error updating profile: {str(e)}")

# Run the function when the script is executed
if __name__ == "__main__":
    change_profile()