import os
import sys

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.humanizer import humanizer_bp
from src.routes.analytics import analytics_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(humanizer_bp)
app.register_blueprint(analytics_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# API catch-all for unhandled /api routes
@app.route("/api/<path:path>")
def api_catch_all(path):
    return jsonify({"error": "API endpoint not found"}), 404

# Serve static files and index.html for all other routes
@app.route('/')
@app.route('/<path:path>')
def serve(path=None):
    if path is None:
        path = ''

    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


