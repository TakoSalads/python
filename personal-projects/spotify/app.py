import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,      # clients require setting up
                                               client_secret=client_secret,  # spotify developer &    - tako
                                               redirect_uri=redirect_uri,  #  modifying the .env file 
                                               scope="playlist-read-private"))

playlist_id = "0uqbFM1bOiBWQhxcBOSKyk"

@app.route("/")
def index():
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]["items"]
    
    playlist_data = {
        "name": playlist["name"],
        "description": playlist["description"],
        "image": playlist["images"][0]["url"] if playlist["images"] else None,
        "tracks": [
            {
                "name": track["track"]["name"],
                "artist": ", ".join(artist["name"] for artist in track["track"]["artists"]),
                "album": track["track"]["album"]["name"],
                "cover": track["track"]["album"]["images"][0]["url"] if track["track"]["album"]["images"] else None
            }
            for track in tracks
        ]
    }
    return render_template("index.html", playlist=playlist_data)

if __name__ == "__main__":
    app.run(debug=True)