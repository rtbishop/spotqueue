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
from itertools import islice
from credentials import *

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    current_song = "No song playing"
    playlist_tracks = None
    user_playlists = None

    user_id = "4392745"
    playlist_id = "3zJTv5sTYzrQuV2gtgO9MG"


    #####################
    ####user playlist####
    #####################

    # if access token is NOT already in the db
    if request.vars.code:
        code = request.vars.code

        payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI}
        encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
        headers = {'Authorization': 'Basic ' + encoded}
        r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
        if r.status_code == 200:
            response = r.json()
            access_token = response['access_token']
            refresh_token = response['refresh_token']
            db(db.auth_user.id == auth.user.id).update(access_token=access_token, refresh_token=refresh_token)
            auth.user.access_token = access_token
            headers = {'Authorization': 'Bearer ' + access_token}

        r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

        if r.status_code == 200:
            content = r.json()
            user_playlists = content['items']
            spotify_user_id = content['items'][0]['owner']['id']
            db(db.auth_user.id == auth.user.id).update(spotify_user_id=spotify_user_id)
            auth.user.spotify_user_id = spotify_user_id

    # if access token is in db
    if auth.user is not None and auth.user.access_token:
        headers = {'Authorization': 'Bearer ' + auth.user.access_token}
        r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

        if r.status_code == 200:
            content = r.json()
            user_playlists = content['items']
        elif r.status_code == 401:
            # refresh access token code goes here
            payload = {'grant_type': 'refresh_token', 'refresh_token': auth.user.refresh_token}
            encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
            headers = {'Authorization': 'Basic ' + encoded}
            r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)

            if r.content:
                response = r.json()
                new_access_token = response['access_token']
                db(db.auth_user.id == auth.user.id).update(access_token=new_access_token)
                auth.user.access_token = new_access_token

    
    ####################################
    ##current song and client playlist##
    ####################################

    payload = {'grant_type': 'client_credentials'}
    encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
    headers = {'Authorization': 'Basic ' + encoded}

    r = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    content = r.json()
    token = content['access_token']

    headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN}
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    headers = {'Authorization': 'Bearer ' + token}
    r2 = requests.get("https://api.spotify.com/v1/users/" + user_id + "/playlists/" + playlist_id + "/tracks", headers=headers)


    if r.status_code == 200:
        content = r.json()
        current_song = content['item']['name']

    if r2.status_code == 200:
        content2 = r2.json()
        playlist_tracks = islice(content2['items'], 4)

    return dict(current_song=current_song,playlist_tracks=playlist_tracks,user_playlists=user_playlists)


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
