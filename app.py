from flask import Flask, render_template, session
#from flask.ext.mongoengine import MongoEngine
import infrastructure
import sys


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'

# db config
#app.config['MONGODB_SETTINGS'] = {'DB': 'testing', 'HOST': 'mongodb://localhost:27017/bookly'}
#db = MongoEngine()
#db.init_app(app)

#setattr(sys.modules['infrastructure'], 'db', db)

# Authentication
from routes.authentication import authentication
app.register_blueprint(blueprint=authentication.auth_app, url_prefix='/authorize')


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
