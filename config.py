import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GITHUB_PAT = os.getenv("GITHUB_PAT")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
