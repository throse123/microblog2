from app import app

@app.route('/')
@app.route('/index')
@app.route('/contact')
@app.route('/cool_poem')
def index():
    return "Hello, World!"
def contact():
    return "My email is throse@packer.edu"
def cool_poem():
    return "The red tiger was in its cage. Yes yes. the tiger it out."

