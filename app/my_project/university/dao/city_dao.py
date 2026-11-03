import os

import mysql.connector
import yaml


class CityDAO:
    def __init__(self):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "app.yml")
        )
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)["database"]

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def find_all(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, name FROM city")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_students_by_city(self, city_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT s.id, s.first_name, s.last_name
                FROM student s
                WHERE s.city_id = %s
            """
            cursor.execute(query, (city_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
