from application import application

@application.route('/')
def hello_world():
    return 'Hello world1!'

@application.route('/about/')
def about():
    return "All about Flask"
