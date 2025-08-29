from app import app

# TODO API here

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"