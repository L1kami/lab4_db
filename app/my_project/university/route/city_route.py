from flask import Blueprint

from my_project.university.controller.city_controller import CityController


city_bp = Blueprint("city_bp", __name__, url_prefix="/api/cities")
controller = CityController()


@city_bp.route("/", methods=["GET"], strict_slashes=False)
def get_cities():
    return controller.get_all()


@city_bp.route("/<int:city_id>/students", methods=["GET"])
def get_students(city_id):
    return controller.get_residents(city_id)
