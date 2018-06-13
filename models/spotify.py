# Spotify model

import base64
import requests
from itertools import islice

class Credentials():

    def __init__(self, client_id, client_secret, client_spotify_user, client_playlist_id,
                 redirect_uri, access_token=None, access_code=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_spotify_user = client_spotify_user
        self.client_playlist_id = client_playlist_id
        self.redirect_uri = redirect_uri
        if access_token is None:
            self.access_token = None
        else:
            self.access_token = access_token
        if access_code is None:
            self.access_code = None
        else:
            self.access_code = access_code
        self.refresh_token = None

    def get_tokens(self):
        if self.access_code is not None:
            payload = {'grant_type': 'authorization_code', 'code': self.access_code, 'redirect_uri': self.redirect_uri}
            headers = {'Authorization': 'Basic ' + base64.b64encode(self.client_id + ":" + self.client_secret)}
            r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
            if r.status_code == 200:
                response = r.json()
                self.access_token = response['access_token']
                self.refresh_token = response['refresh_token']
        return dict(access_token=self.access_token, refresh_token=self.refresh_token)

class Spotify(object):

    def __init__(self, credentials_manager):
        self.credentials_manager = credentials_manager
        self.tokens = self.credentials_manager.get_tokens()
        self.access_token = self.tokens['access_token']
        self.refresh_token = self.tokens['refresh_token']
        self.client_spotify_user = self.credentials_manager.client_spotify_user
        self.client_playlist_id = self.credentials_manager.client_playlist_id

    def get_currently_playing(self):
        current_song = {"item": {"name": "No song playing"}}
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
        if r.status_code == 200:
            response = r.json()
            if response is not None:
                current_song = response
        return current_song

    def get_playlist_tracks(self):
        playlist_tracks = None
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/users/" + self.client_spotify_user + "/playlists/" +
                         self.client_playlist_id + "/tracks", headers=headers)
        if r.status_code == 200:
            response = r.json()
            playlist_tracks = islice(response['items'], 4)
        return playlist_tracks

    def search_songs(self, query):
        songs = None
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/search?q=" + query + "&type=track&limit=5", headers=headers)
        if r.status_code == 200:
            response = r.json()
            songs = response['tracks']['items']
        return songs

    def add_to_queue(self, song_uri):
        response = None
        headers = {'Authorization': 'Bearer ' + self.access_token, 'Content-Type': 'application/json'}
        r = requests.post("https://api.spotify.com/v1/users/" + self.client_spotify_user + "/playlists/" +
                          self.client_playlist_id + "/tracks?uris=" + song_uri, headers=headers)
        if r.status_code == 200:
            response = r.json()
        return response

    # user methods
    def get_spotify_user_id(self):
        spotify_user_id = None
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        if r.status_code == 200:
            response = r.json()
            spotify_user_id = response['items'][0]['owner']['id']
        return spotify_user_id

    def get_playlists(self):
        user_playlists = None
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        if r.status_code == 200:
            response = r.json()
            user_playlists = response['items']
        return user_playlists

    def get_tracks(self, playlist_id):
        tracks_in_playlist = None
        headers = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get("https://api.spotify.com/v1/users/" + self.get_spotify_user_id() + "/playlists/" +
                         playlist_id + "/tracks", headers=headers)
        if r.status_code == 200:
            response = r.json()
            tracks_in_playlist = response['items']
        return tracks_in_playlist
