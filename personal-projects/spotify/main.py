import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=" ".join(scopes)))

# Playlist ID
playlist_id = "0uqbFM1bOiBWQhxcBOSKyk"

# Track storage
track_uris = []


# Get currently playing track
def get_current_track():
    current_track = sp.current_user_playing_track()
    if current_track and current_track["item"]:
        track_uri = current_track["item"]["uri"]
        track_uris.append(track_uri)
        print("Success! Currently playing:", current_track["item"]["name"])
    else:
        print("Failed! - no song playing or utter failure")


# Get recently played tracks
def get_recent():
    recently_played = sp.current_user_recently_played(limit=10)
    new_tracks = [item["track"]["uri"] for item in recently_played["items"]]
    return new_tracks


# Gather all tracks (current + recent)
def combination():
    track_uris.extend(get_recent())


# Add songs to playlist and maintain exactly 50 songs
def add_items():
    if not track_uris:
        print("GFYS")
        return

    # Remove duplicates while keeping order
    no_dupe_tracks = list(dict.fromkeys(track_uris))

    # Get current playlist tracks
    existing_tracks = sp.playlist_tracks(playlist_id)["items"]
    existing_uris = [item["track"]["uri"] for item in existing_tracks]

    # Separate tracks that need to be repositioned vs new additions
    reposition_tracks = [track for track in no_dupe_tracks if track in existing_uris]
    new_tracks = [track for track in no_dupe_tracks if track not in existing_uris]

    # Move existing tracks to the top
    if reposition_tracks:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, reposition_tracks)
        time.sleep(1)
        sp.playlist_add_items(playlist_id=playlist_id, items=reposition_tracks, position=0)
        print(f"Moved {len(reposition_tracks)} existing tracks to the top!")

    # Add new tracks to the top
    if new_tracks:
        sp.playlist_add_items(playlist_id=playlist_id, items=new_tracks, position=0)
        print(f"Added {len(new_tracks)} new tracks to the playlist!")

    # Ensure playlist is exactly 50 songs
    playlist_organize()


# Organize playlist to maintain exactly 50 songs
def playlist_organize():
    max_songs = 50

    # Get current playlist tracks
    existing_tracks = sp.playlist_tracks(playlist_id=playlist_id)["items"]
    current_uris = [item["track"]["uri"] for item in existing_tracks]

    if len(current_uris) > max_songs:
        # Remove oldest songs beyond the limit
        tracks_to_remove = current_uris[max_songs:]
        sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_to_remove)
        print(f"Removed {len(tracks_to_remove)} oldest tracks to maintain 50-song limit.")
    elif len(current_uris) < max_songs:
        print(f"Warning: Playlist has only {len(current_uris)} songs instead of 50. Ensure enough tracks are being gathered.")
    else:
        print("Playlist is correctly at 50 songs.")


# Run functions
get_current_track()
combination()
add_items()
 