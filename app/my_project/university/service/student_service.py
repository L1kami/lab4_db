from my_project.university.dao.student_dao import StudentDAO
from my_project.university.domain.student_dto import StudentDTO


class StudentService:
    def __init__(self):
        self.dao = StudentDAO()

    def get_all(self):
        students = self.dao.find_all()
        return [
            StudentDTO(
                student["id"],
                student["first_name"],
                student["last_name"],
                student["city_id"],
            ).to_dict()
            for student in students
        ]

    def get_by_id(self, student_id):
        student = self.dao.find_by_id(student_id)
        if not student:
            return None
        return StudentDTO(
            student["id"],
            student["first_name"],
            student["last_name"],
            student["city_id"],
        ).to_dict()

    def create(self, data):
        return self.dao.create(data)

    def update(self, student_id, data):
        self.dao.update(student_id, data)

    def delete(self, student_id):
        self.dao.delete(student_id)

    def get_student_courses(self, student_id):
        return self.dao.get_courses_by_student(student_id)
