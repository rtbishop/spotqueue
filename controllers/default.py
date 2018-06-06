# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import spotipy
import spotipy.util as util
from credentials import CLIENT_ID, CLIENT_SECRET, PLAYLIST_ID, SPOTIFY_USER

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict()


def test():
    scope = "user-read-currently-playing"
    redirect_uri = "http://127.0.0.1:8000/spotqueue/default/test"
    token = util.prompt_for_user_token(SPOTIFY_USER, scope = scope, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = redirect_uri)
    spotify = spotipy.Spotify(auth = token)
    songs = spotify.currently_playing(market = None)


    # results1['items'][0]['track']['name']
    # token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # cache_token = token.get_access_token()
    # spotify = spotipy.Spotify(cache_token)
    # songs = spotify.user_playlist_tracks(SPOTIFY_USER, PLAYLIST_ID, limit=100, offset=0)
    return dict(songs=songs)


def about():

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
