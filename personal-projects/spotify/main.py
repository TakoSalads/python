#tako - 26/02/2025 
#project goals:
# * access the spotify user data by using spotipy.
# * create a playlist based on previous listening data (multiple based on varible timings.)
# * update on program launch, create save point if enjoying.
#
#tentative features:
# * full tkinter gui
# * passive playlist updates
# * take in multiple sets of data (current listening, playlist relation, spotify mix related to current listening)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,      # Both require setting up
                                               client_secret=client_secret,  # spotify developer
                                               redirect_uri=redirect_uri,
                                               scope=" ".join(scopes)))

#playlist ID
playlist_id = "0uqbFM1bOiBWQhxcBOSKyk"

#store current tracks
track_uris = []

#gathering songs
def get_current_track():
    current_track = sp.current_user_playing_track()
    if current_track and current_track["item"]:
        track_uri = current_track["item"]["uri"]
        track_uris.append(track_uri)
        print("Success! Currently playing:", current_track["item"]["name"])
    else:
        print("Failed! - no song playing or utter failure")

def get_recent():
    recently_played = sp.current_user_recently_played(limit=10, after=None, before=None)
    new_tracks = [item["track"]["uri"] for item in recently_played["items"]]
    return new_tracks

def combination():
    track_uris.extend(get_recent())

#adding to playlist
def add_items():
    if track_uris:
        noDupe = list(dict.fromkeys(track_uris))

        existing_tracks = sp.playlist_tracks(playlist_id)["items"]
        existing_urls = [item["track"]["uri"] for item in existing_tracks]

        new_tracks = [track for track in noDupe if track not in existing_urls]

        if new_tracks:
            sp.playlist_add_items(playlist_id=playlist_id, items=noDupe)
            print(f"Added {len(noDupe)} tracks to the playlist!")
        else:
            print("No new tracks to add.")
    else:
        print("GFYS")

        


get_current_track()
get_recent()
combination()
add_items()




