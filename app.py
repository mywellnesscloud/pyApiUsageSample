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
from areas.user.auth import user_app
app.register_blueprint(blueprint=user_app, url_prefix='/user')


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


if __name__ == '__main__':
    app.run()
