from app import app

@app.route('/')
def hello_world():
    return 'Hello world1!'

@app.route('/about')
def about():
    return "All about Flask"
