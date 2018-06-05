# Here go your api methods.

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

def get_songs():
    print 'made it to get_songs'
    songs = []
    rows = db(auth.user_id == db.songs.added_by).select(db.songs.ALL, orderby=~db.songs.created_on, limitby=(0,20))
    for r in rows:
            t = dict(
            	added_by = r.added_by,
            	created_on = r.created_on,
            	song_url = r.song_url,
                name_ = r.name_,
                id = r.id,
            )
            songs.append(t)
    return response.json(dict(
        songs = songs,
        ))
