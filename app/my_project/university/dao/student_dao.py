import os

import mysql.connector
import yaml


class StudentDAO:
    def __init__(self):
        config_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "config", "app.yml"
            )
        )
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)["database"]

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def find_all(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, first_name, last_name, city_id FROM student"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, first_name, last_name, city_id
                FROM student
                WHERE id = %s
                """,
                (student_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def create(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO student (first_name, last_name, city_id)
                VALUES (%s, %s, %s)
                """,
                (data["first_name"], data["last_name"], data["city_id"]),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def update(self, student_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE student
                SET first_name = %s, last_name = %s, city_id = %s
                WHERE id = %s
                """,
                (
                    data["first_name"],
                    data["last_name"],
                    data["city_id"],
                    student_id,
                ),
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_courses_by_student(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.title
                FROM course c
                JOIN student_course sc ON c.id = sc.course_id
                WHERE sc.student_id = %s
                """,
                (student_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
