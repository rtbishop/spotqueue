# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

def get_user_first_name():
	return auth.user.first_name if auth.user else None


db.define_table('songs',
                Field('id'),
                Field('created_on', 'datetime', default=request.now),
				Field('added_by', 'reference auth_user', default=auth.user_id),
				Field('name_', default=get_user_first_name()),
				Field('song_name'),
                Field('song_image'),
                )


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.auth_user.access_token.writable = False
#db.auth_user.access_token.readable = False
db.auth_user.refresh_token.writable = False
#db.auth_user.refresh_token.readable = False
db.auth_user.spotify_user_id.writable = False