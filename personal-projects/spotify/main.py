#tako - 25/02/2025 
#project goals:
# * access the spotify user data by using spotipy.
# * create a playlist based on previous listening data (multiple based on varible timings.)
# * update on program launch, create save point if enjoying.
#
#tentative features:
# * full tkinter gui
# * passive playlist updates
# * take in multiple sets of data (current listening, playlist relation, spotify mix related to current listening)
#
#tako - 27/02/2025
#current build
# * project goals complete besides save-points (not enough listening data currently)
# * playlist limit set to 50, appends newest listen removes oldest.
# * updates automatically upon program launch.
# * uses flask & bootstrap instead of tkinter - dynamic updates & clean interface


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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,      # clients require setting up
                                               client_secret=client_secret,  # spotify developer &    - tako
                                               redirect_uri=redirect_uri,  #  modifying the .env file 
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
            print(f"Added {len(new_tracks)} tracks to the playlist!")

            playlist_organize(new_tracks)
        else:
            print("No new tracks to add.")
    else:
        print("GFYS")

def playlist_organize(new_tracks):
    max_songs = 50

    existing_tracks = sp.playlist_tracks(playlist_id=playlist_id)["items"]
    current_tracks = [item["track"]["uri"] for item in existing_tracks]

    all_tracks = current_tracks + new_tracks

    if len(all_tracks) > max_songs:
        tracks_remove = len(all_tracks) - max_songs
        tracks_remove_uris = all_tracks[:tracks_remove]

        sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_remove_uris)
        print(f"Removed {tracks_remove} tracks to keep playlist within limit.")

    else:
        print("Playlist within parameters.")

        

get_current_track()
get_recent()
combination()
add_items()




