import os
import tweepy
from flask import Flask, redirect, request, session

app = Flask(__name__)

# Force Flask to use production mode
app.config["ENV"] = "production"
app.config["DEBUG"] = False

@app.route("/")
def home():
    print("✅ Home route accessed")
    return "✅ Twitter Bot is Running on Letmein!"

@app.route("/callback", methods=["GET"])
def callback():
    """Debugging: Check if this route is detected"""
    print("✅ Callback route accessed")
    return "✅ Callback route is working!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure correct port
    print(f"🚀 Starting Flask on port {port}...")
    app.run(host="0.0.0.0", port=port)