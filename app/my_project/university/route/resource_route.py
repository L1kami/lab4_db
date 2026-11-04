from flask import Blueprint

from my_project.university.controller.entity_controller import EntityController
from my_project.university.dao.entity_daos import (
    AirlineDAO, AirportDAO, BaggageRuleDAO, BookingDAO, BookingStatusDAO,
    CityDAO, ConnectedFlightDAO, CountryDAO, FlightDAO, TicketDAO, UserDAO,
)
from my_project.university.domain.models import (
    Airline, Airport, BaggageRule, Booking, BookingStatus, City,
    ConnectedFlight, Country, Flight, Ticket, User,
)
from my_project.university.service.entity_service import EntityService


api_bp = Blueprint("api", __name__, url_prefix="/api")

RESOURCES = {
    "countries": (CountryDAO, Country),
    "cities": (CityDAO, City),
    "airports": (AirportDAO, Airport),
    "airlines": (AirlineDAO, Airline),
    "baggage-rules": (BaggageRuleDAO, BaggageRule),
    "users": (UserDAO, User),
    "booking-statuses": (BookingStatusDAO, BookingStatus),
    "bookings": (BookingDAO, Booking),
    "flights": (FlightDAO, Flight),
    "connected-flights": (ConnectedFlightDAO, ConnectedFlight),
    "tickets": (TicketDAO, Ticket),
}


def register_resource(resource_name, dao_type, dto_type):
    controller = EntityController(EntityService(dao_type(), dto_type))
    endpoint = resource_name.replace("-", "_")
    api_bp.add_url_rule(
        f"/{resource_name}", endpoint=f"{endpoint}_list", view_func=controller.get_all, methods=["GET"]
    )
    api_bp.add_url_rule(
        f"/{resource_name}", endpoint=f"{endpoint}_create", view_func=controller.create, methods=["POST"]
    )
    api_bp.add_url_rule(
        f"/{resource_name}/<int:item_id>", endpoint=f"{endpoint}_get",
        view_func=controller.get_by_id, methods=["GET"]
    )
    api_bp.add_url_rule(
        f"/{resource_name}/<int:item_id>", endpoint=f"{endpoint}_update",
        view_func=controller.update, methods=["PUT"]
    )
    api_bp.add_url_rule(
        f"/{resource_name}/<int:item_id>", endpoint=f"{endpoint}_delete",
        view_func=controller.delete, methods=["DELETE"]
    )


for resource, (dao_type, dto_type) in RESOURCES.items():
    register_resource(resource, dao_type, dto_type)
