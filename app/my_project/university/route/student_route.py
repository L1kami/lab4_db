from flask import Blueprint

from my_project.university.controller.student_controller import StudentController


student_bp = Blueprint("student_bp", __name__, url_prefix="/api/students")
controller = StudentController()


@student_bp.route("", methods=["GET"])
@student_bp.route("/", methods=["GET"], strict_slashes=False)
def get_students():
    return controller.get_all()


@student_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    return controller.get_by_id(student_id)


@student_bp.route("", methods=["POST"])
@student_bp.route("/", methods=["POST"], strict_slashes=False)
def create_student():
    return controller.create()


@student_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    return controller.update(student_id)


@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    return controller.delete(student_id)


@student_bp.route("/<int:student_id>/courses", methods=["GET"])
def get_student_courses(student_id):
    return controller.get_courses(student_id)
