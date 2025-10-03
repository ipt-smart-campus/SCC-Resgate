from flask import Flask
import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from controllers.occupancy_controller import occupancy_bp
from config import config


def create_app() -> Flask:
    app = Flask(__name__)

    # Blueprints
    app.register_blueprint(occupancy_bp)

    # Informações de configuração mínimas expostas (para templates/diagnóstico)
    @app.context_processor
    def inject_conf():
        return {
            "API_BASE": config.API_BASE,
            "API_SPACES_ENDPOINT": config.API_SPACES_ENDPOINT,
        }

    return app


if __name__ == "__main__":
    app = create_app()
    # Em produção, use um servidor WSGI (gunicorn/uwsgi). Debug=True só para desenvolvimento.
    app.run(host="0.0.0.0", port=8081, debug=True)
