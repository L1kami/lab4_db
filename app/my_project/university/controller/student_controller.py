from flask import jsonify, request

from my_project.university.service.student_service import StudentService


class StudentController:
    def __init__(self):
        self.service = StudentService()

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, student_id):
        student = self.service.get_by_id(student_id)
        if student is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(student), 200

    def create(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body is required"}), 400
        student_id = self.service.create(data)
        return jsonify({"id": student_id, "message": "Created successfully"}), 201

    def update(self, student_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body is required"}), 400
        if self.service.get_by_id(student_id) is None:
            return jsonify({"error": "Not found"}), 404
        self.service.update(student_id, data)
        return jsonify({"message": "Updated successfully"}), 200

    def delete(self, student_id):
        if self.service.get_by_id(student_id) is None:
            return jsonify({"error": "Not found"}), 404
        self.service.delete(student_id)
        return jsonify({"message": "Deleted successfully"}), 200

    def get_courses(self, student_id):
        if self.service.get_by_id(student_id) is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(self.service.get_student_courses(student_id)), 200
