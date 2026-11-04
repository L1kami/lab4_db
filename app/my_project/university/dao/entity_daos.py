from .crud_dao import CRUDDAO


class CountryDAO(CRUDDAO):
    table, columns, required_columns = "countries", ("name",), ("name",)


class CityDAO(CRUDDAO):
    table, columns, required_columns = "cities", ("country_id", "name"), ("country_id", "name")


class AirportDAO(CRUDDAO):
    table, columns, required_columns = "airports", ("city_id", "iata_code", "name"), ("city_id", "iata_code", "name")


class AirlineDAO(CRUDDAO):
    table, columns, required_columns = "airlines", ("name", "base_airport_id", "contact_email"), ("name", "base_airport_id")


class BaggageRuleDAO(CRUDDAO):
    table, columns, required_columns = "baggage_rules", ("airline_id", "tier_name", "weight_limit_kg"), ("airline_id", "tier_name", "weight_limit_kg")


class UserDAO(CRUDDAO):
    table, columns, required_columns = "users", ("first_name", "last_name", "email", "phone"), ("first_name", "last_name", "email")


class BookingStatusDAO(CRUDDAO):
    table, columns, required_columns = "booking_statuses", ("status_name",), ("status_name",)


class BookingDAO(CRUDDAO):
    table, columns, required_columns = "bookings", ("user_id", "status_id", "booking_date", "total_price"), ("user_id", "status_id", "total_price")


class FlightDAO(CRUDDAO):
    table, columns, required_columns = "flights", ("airline_id", "dep_airport_id", "arr_airport_id", "departure_time", "arrival_time", "base_price", "baggage_rule_id"), ("airline_id", "dep_airport_id", "arr_airport_id", "departure_time", "arrival_time", "base_price", "baggage_rule_id")


class ConnectedFlightDAO(CRUDDAO):
    table, columns, required_columns = "connected_flights", ("flight_1_id", "flight_2_id", "layover_duration_mins"), ("flight_1_id", "flight_2_id", "layover_duration_mins")


class TicketDAO(CRUDDAO):
    table, columns, required_columns = "tickets", ("booking_id", "flight_id", "passenger_name", "seat_number"), ("booking_id", "flight_id", "passenger_name", "seat_number")
