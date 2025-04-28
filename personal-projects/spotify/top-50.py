import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
import json

# Load environment variables
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

scopes = [
    "user-read-currently-playing",
    "user-read-recently-played",
    "playlist-modify-private",
    "playlist-read-private"
]

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=" ".join(scopes)))

playlist_id = 'https://open.spotify.com/playlist/0m2CspvZYTfqiEjvzGxhkW'
playlist_id_recently_listened = "0uqbFM1bOiBWQhxcBOSKyk"


# Track storage
track_uris = []

# Safe API call with retries
def safe_spotify_call(func, *args, **kwargs):
    retries = 3
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error on attempt {attempt+1}: {e}")
            time.sleep(5)
    print("Max retries reached, skipping operation.")
    return None


def get_current_counts():
    with open('logs/recentlylistened.json', 'r') as f:
 
            




#idea:
#take the each song added to recently-listened, assign a digit each time it appears, having the 50 most appearing
#append into a new playlist called top 50