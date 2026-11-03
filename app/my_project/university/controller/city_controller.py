from flask import jsonify

from my_project.university.service.city_service import CityService


class CityController:
    def __init__(self):
        self.service = CityService()

    def get_all(self):
        cities = self.service.get_all_cities()
        return jsonify(cities), 200

    def get_residents(self, city_id):
        residents = self.service.get_city_residents(city_id)
        return jsonify(residents), 200
