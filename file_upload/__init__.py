from flask import Flask

from file_upload import pages
from file_upload import templates

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'myPonney'
    
    app.register_blueprint(pages.bp)

    app.register_blueprint(templates.bp)

    return app