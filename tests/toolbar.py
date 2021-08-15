#requirements:
flask-debugtoolbar


app.debug = True
app.config['SECRET_KEY'] = 'asdfasdfds'
toolbar = DebugToolbarExtension(app)

