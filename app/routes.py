from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'thomas'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='home',user=user, posts=posts)

@app.route('/contact')
def contact():
    return "My email is throse@packer.edu"

@app.route('/cool_poem')
def cool_poem():
    return '''
<html>
    <head
        <title>Here is a cool poem</title>
    </head>
    <body>
    "The red tiger is in its cage. yes Yes. the tiger is out."
    </body>
</html>'''

