from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


class DTO:
    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        return {
            key: (item.isoformat(sep=" ") if isinstance(item, datetime) else
                  float(item) if isinstance(item, Decimal) else item)
            for key, item in value.items()
        }


@dataclass
class Country(DTO):
    id: int | None = None
    name: str = ""


@dataclass
class City(DTO):
    id: int | None = None
    country_id: int = 0
    name: str = ""


@dataclass
class Airport(DTO):
    id: int | None = None
    city_id: int = 0
    iata_code: str = ""
    name: str = ""


@dataclass
class Airline(DTO):
    id: int | None = None
    name: str = ""
    base_airport_id: int = 0
    contact_email: str | None = None


@dataclass
class BaggageRule(DTO):
    id: int | None = None
    airline_id: int = 0
    tier_name: str = ""
    weight_limit_kg: int = 0


@dataclass
class User(DTO):
    id: int | None = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str | None = None


@dataclass
class BookingStatus(DTO):
    id: int | None = None
    status_name: str = ""


@dataclass
class Booking(DTO):
    id: int | None = None
    user_id: int = 0
    status_id: int = 0
    booking_date: datetime | None = None
    total_price: Decimal | float = 0


@dataclass
class Flight(DTO):
    id: int | None = None
    airline_id: int = 0
    dep_airport_id: int = 0
    arr_airport_id: int = 0
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    base_price: Decimal | float = 0
    baggage_rule_id: int = 0


@dataclass
class ConnectedFlight(DTO):
    id: int | None = None
    flight_1_id: int = 0
    flight_2_id: int = 0
    layover_duration_mins: int = 0


@dataclass
class Ticket(DTO):
    id: int | None = None
    booking_id: int = 0
    flight_id: int = 0
    passenger_name: str = ""
    seat_number: str = ""
