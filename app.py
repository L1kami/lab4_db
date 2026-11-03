import os
import sys

from flask import Flask

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from my_project.university.route.city_route import city_bp
from my_project.university.route.student_route import student_bp


app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(city_bp)
app.register_blueprint(student_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
