import os
import sys

from flask import Flask

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from my_project.university.route.resource_route import api_bp


app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
