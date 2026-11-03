class StudentDTO:
    def __init__(self, id, first_name, last_name, city_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.city_id = city_id

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "city_id": self.city_id,
        }
