from flask import jsonify, request


class EntityController:
    def __init__(self, service):
        self.service = service

    def get_all(self):
        return jsonify(self.service.get_all()), 200

    def get_by_id(self, item_id):
        item = self.service.get_by_id(item_id)
        return (jsonify(item), 200) if item else (jsonify({"error": "Not found"}), 404)

    def create(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "JSON object is required"}), 400
        try:
            item_id = self.service.create(data)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify({"id": item_id, "message": "Created successfully"}), 201

    def update(self, item_id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "JSON object is required"}), 400
        if self.service.get_by_id(item_id) is None:
            return jsonify({"error": "Not found"}), 404
        try:
            self.service.update(item_id, data)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify({"message": "Updated successfully"}), 200

    def delete(self, item_id):
        if self.service.get_by_id(item_id) is None:
            return jsonify({"error": "Not found"}), 404
        self.service.delete(item_id)
        return jsonify({"message": "Deleted successfully"}), 200
