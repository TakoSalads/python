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

scopes = [
    "user-read-currently-playing",
    "user-read-recently-played",
    "playlist-modify-private",
    "playlist-read-private"
]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="41672c6c7c034a7b8c39f7c8af6bb467",      # Both require setting up
                                               client_secret="081c4f7b7cee46b393ad4022c234d560",  # spotify developer
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=" ".join(scopes)))

current_track = sp.current_user_playing_track()
if current_track:
    print("Success! Currently playing:", current_track["item"]["name"])
else:
    print("Failed! - no song playing or utter failure")

recently_played = sp.current_user_recently_played(limit=10, after=None, before=None)
for idx, item in enumerate(recently_played["items"]):
    track = item["track"]
    song_name = track["name"]
    artist_name = track["artists"][0]["name"]
    played_at = item["played_at"] 

    print(f"{idx+1}. {song_name} by {artist_name} - (Played at: {played_at})")

