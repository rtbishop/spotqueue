# Here go your api methods.

def get_initial_data():
    print 'made it here'
    a = ["a" + str(i) for i in range(10)]
    logged_in = auth.user_id is not None
    return response.json(dict(
        logged_in = logged_in,
        animals = ['dog', 'cat', 'fish'],
        things = ['thing1', 'thing2', 'thing3'],
        other_things = a,
    ))
