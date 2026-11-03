from my_project.university.dao.city_dao import CityDAO
from my_project.university.domain.city_dto import CityDTO


class CityService:
    def __init__(self):
        self.dao = CityDAO()

    def get_all_cities(self):
        cities_data = self.dao.find_all()
        return [CityDTO(city["id"], city["name"]).to_dict() for city in cities_data]

    def get_city_residents(self, city_id):
        return self.dao.get_students_by_city(city_id)
