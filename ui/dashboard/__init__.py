import os
from flask import Flask

# function that creates a web app
def create_app():
    app = Flask(__name__)

    # importing views module -> practice to prevent circular references
    from . import views
    app.register_blueprint(views.bp)

    return app
