# Here go your api methods.

import requests
import base64
from credentials import CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI, CLIENT_ACCESS_TOKEN

client_credentials = Credentials(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI,
                                     CLIENT_ACCESS_TOKEN)
spotify = Spotify(client_credentials)

def search_songs():
    query = None
    query = request.vars.query
    songs = spotify.search_songs(query)
    return response.json(dict(songs=songs))

def add_to_queue():
    song_uri = None
    song_uri = request.vars.song_uri
    add_to_queue = spotify.add_to_queue(song_uri)
    session.flash = T("Success! Song added to the queue")
    return add_to_queue

def get_playlists():
    user_playlists = None

    headers = {'Authorization': 'Bearer ' + auth.user.access_token}
    r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    if r.content:
        content = r.json()
        user_playlists = content['items']

    return response.json(dict(user_playlists=user_playlists))

def get_tracks():
    playlist_id = None
    playlist_id = request.vars.playlist_id
    tracks_in_playlist = None

    headers = {'Authorization': 'Bearer ' + auth.user.access_token}
    r = requests.get("https://api.spotify.com/v1/users/" + auth.user.spotify_user_id + "/playlists/" + playlist_id + "/tracks", headers=headers)

    if r.content:
        content = r.json()
        tracks_in_playlist = content['items']

    return response.json(dict(tracks_in_playlist=tracks_in_playlist))



def get_initial_data():
    print 'made it here'
    current_user = None
    logged_in = auth.user_id is not None
    if logged_in:
        current_user = auth.user.first_name
    print current_user
    print logged_in
    return response.json(dict(
        logged_in = logged_in,
        current_user = current_user,
    ))

# def get_songs():
#     print 'made it to get_songs'
#     songs = []
#     rows = db(auth.user_id == db.songs.added_by).select(db.songs.ALL, orderby=~db.songs.created_on, limitby=(0,20))
#     for r in rows:
#             t = dict(
#             	added_by = r.added_by,
#             	created_on = r.created_on,
#             	song_url = r.song_url,
#                 name_ = r.name_,
#                 id = r.id,
#             )
#             songs.append(t)
#     return response.json(dict(
#         songs = songs,
#         ))