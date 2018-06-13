# Here go your api methods.

import requests
import base64
from credentials import CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI, CLIENT_ACCESS_TOKEN

client_credentials = Credentials(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI,
                                     CLIENT_ACCESS_TOKEN)
client = Spotify(client_credentials)

if auth.user:
    user_credentials = Credentials(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI, auth.user.access_token)
    user = Spotify(user_credentials)

def search_songs():
    query = None
    query = request.vars.query
    songs = client.search_songs(query)
    return response.json(dict(songs=songs))

def add_to_queue():
    song_uri = None
    song_uri = request.vars.song_uri
    add_to_queue = client.add_to_queue(song_uri)
    session.flash = T("Success! Song added to the queue")
    return add_to_queue

def get_playlists():
    user_playlists = user.get_playlists()
    return response.json(dict(user_playlists=user_playlists))

def get_tracks():
    playlist_id = None
    playlist_id = request.vars.playlist_id
    tracks_in_playlist = user.get_tracks(playlist_id)
    return response.json(dict(tracks_in_playlist=tracks_in_playlist))

def get_initial_data():
    current_user = None
    logged_in = auth.user_id is not None
    if logged_in:
        current_user = auth.user.first_name
    return response.json(dict(
        logged_in = logged_in,
        current_user = current_user,
    ))