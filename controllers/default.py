# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import requests
from credentials import CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI, CLIENT_ACCESS_TOKEN

client_credentials = Credentials(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI,
                                     CLIENT_ACCESS_TOKEN)
client = Spotify(client_credentials)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    current_song = client.get_currently_playing()
    playlist_tracks = client.get_playlist_tracks()

    # connecting new users to Spotify
    if request.vars.code and auth.user.access_token is None:
        user_credentials = Credentials(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER, PLAYLIST_ID, REDIRECT_URI, None,
                                       request.vars.code)
        user = Spotify(user_credentials)

        access_token = user.access_token
        refresh_token = user.refresh_token
        db(db.auth_user.id == auth.user.id).update(access_token=access_token, refresh_token=refresh_token)
        auth.user.access_token = access_token

        spotify_user_id = user.get_spotify_user_id()
        db(db.auth_user.id == auth.user.id).update(spotify_user_id=spotify_user_id)
        auth.user.spotify_user_id = spotify_user_id

    return dict(current_song=current_song,playlist_tracks=playlist_tracks)


def callback():
     scope = "playlist-read-private"
     payload = {'client_id': CLIENT_ID, 'response_type': 'code', 'redirect_uri': REDIRECT_URI, 'scope': scope}
     response = requests.get("https://accounts.spotify.com/authorize", params=payload)
     redirect(response.url)

def about():
    return dict()

def team():
    return dict()

def faq():
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    # auth.settings.login_next = URL('default', 'callback')
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
