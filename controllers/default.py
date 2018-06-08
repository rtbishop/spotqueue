# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import base64
import requests
import spotipy.util as util
from itertools import islice
from credentials import CLIENT_ID, CLIENT_SECRET, SPOTIFY_USER

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    current_song = "No song playing"
    playlist_tracks = None

    # if request.vars.code:
    #     code = request.vars.code
    #     redirect_uri = "http://127.0.0.1:8000/spotqueue/default/index"
    #     user_id = "4392745"
    #     playlist_id = "3zJTv5sTYzrQuV2gtgO9MG"

        # payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
        # encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
        # headers = {'Authorization': 'Basic ' + encoded}
        # r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
        # response = r.json()
        # token = response['access_token']
        # headers = {'Authorization': 'Bearer ' + token}
        # r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
        # r2 = requests.get("https://api.spotify.com/v1/users/"+user_id+"/playlists/"+playlist_id+"/tracks", headers=headers)

    user_id = "4392745"
    playlist_id = "3zJTv5sTYzrQuV2gtgO9MG"
    payload = {'grant_type': 'client_credentials'}
    encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
    headers = {'Authorization': 'Basic ' + encoded}

    r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    content = r.json()
    token = content['access_token']

    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get("https://api.spotify.com/v1/users/" + user_id + "/playlists/" + playlist_id + "/tracks", headers=headers)

        # if r.content:
            # content = r.json()
            # artist = content['item']['artists'][0]['name']
            # track = content['item']['name']
            # track_id = content['item']['id']
            # current_song = track + " - " + artist
            # content2 = r2.json()
            # playlist_tracks = islice(content2['items'], 3)

    if r.content:
        content = r.json()
        current_song = content['items'][0]['track']['name']
        playlist_tracks = islice(content['items'], 4)

    return dict(current_song=current_song,playlist_tracks=playlist_tracks)


def callback():

    # scope = "user-read-currently-playing"
    # redirect_uri = "http://127.0.0.1:8000/spotqueue/default/index"
    # token = util.prompt_for_user_token(SPOTIFY_USER, scope, client_id=CLIENT_ID,
    #                                    client_secret=CLIENT_SECRET, redirect_uri=redirect_uri)
    #
    # return "ok"
    redirect(URL('default', 'index'))


def test():

    song = None

    return dict(songs=song)


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
    auth.settings.login_next = URL('default', 'callback')
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
