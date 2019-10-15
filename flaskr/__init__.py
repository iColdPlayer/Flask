import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from flaskr import db
    db.init_app(app)
    #register our new app to init file so they can handle the request
    from flaskr import auth, blog
    app.register_blueprint(auth.bp) #import login and register to our app
    app.register_blueprint(blog.bp) #import blog app to our app
    app.add_url_rule('/', endpoint='index') #adding the url rule for our blog app


    return app


