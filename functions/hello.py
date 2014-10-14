import bobo

@bobo.query('/')
def hello(person):
    return 'Hello %s!' % person
