from flask import Flask
from flask_cors import CORS

from .controller.index_controller import module
from .controller.payments_controller import payments_blueprint


webapp = Flask(__name__)
CORS(webapp)
webapp.config.from_object('config.config')

# webapp.register_blueprint(module)
webapp.register_blueprint(payments_blueprint)

