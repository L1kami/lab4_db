import mysql.connector
import yaml
import os

class CityDAO:
    def __init__(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../app/config/app.yml'))
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)['database']

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def find_all(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM city")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_students_by_city(self, city_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.id, s.first_name, s.last_name 
            FROM student s 
            WHERE s.city_id = %s
        """
        cursor.execute(query, (city_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result