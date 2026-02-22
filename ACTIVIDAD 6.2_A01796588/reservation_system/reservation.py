"""Module for Reservation class with persistent storage."""
import json
import os

from reservation_system.hotel import Hotel
from reservation_system.customer import Customer


class Reservation:
    """Represents a reservation linking a customer to a hotel."""

    DATA_FILE = os.path.join("data", "reservations.json")

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initialize a Reservation instance.

        Args:
            reservation_id: Unique identifier for the reservation.
            customer_id: ID of the customer making the reservation.
            hotel_id: ID of the hotel being reserved.
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convert reservation instance to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Reservation instance from a dictionary.

        Args:
            data: Dictionary with reservation attributes.

        Returns:
            Reservation instance or None if data is invalid.
        """
        try:
            required = ["reservation_id", "customer_id", "hotel_id"]
            for field in required:
                if field not in data:
                    print(
                        f"Error: Missing field '{field}' "
                        "in reservation data."
                    )
                    return None
            return cls(
                data["reservation_id"],
                data["customer_id"],
                data["hotel_id"],
            )
        except (TypeError, KeyError) as exc:
            print(f"Error creating reservation from data: {exc}")
            return None

    @staticmethod
    def _load_all(data_file=None):
        """Load all reservations from the JSON file.

        Args:
            data_file: Optional path to the data file.

        Returns:
            List of reservation dictionaries.
        """
        file_path = data_file or Reservation.DATA_FILE
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    print(
                        "Error: Reservation data file has invalid format."
                    )
                    return []
                return data
        except json.JSONDecodeError as exc:
            print(f"Error reading reservation data file: {exc}")
            return []
        except OSError as exc:
            print(f"Error accessing reservation data file: {exc}")
            return []

    @staticmethod
    def _save_all(reservations, data_file=None):
        """Save all reservations to the JSON file.

        Args:
            reservations: List of reservation dictionaries to save.
            data_file: Optional path to the data file.
        """
        file_path = data_file or Reservation.DATA_FILE
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(reservations, file, indent=2)

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id,
                           data_file=None, hotel_file=None,
                           customer_file=None):
        """Create a new reservation.

        Validates that the customer and hotel exist, and that a room
        is available before creating the reservation.

        Args:
            reservation_id: Unique identifier for the reservation.
            customer_id: ID of the customer.
            hotel_id: ID of the hotel.
            data_file: Optional path to the reservations data file.
            hotel_file: Optional path to the hotels data file.
            customer_file: Optional path to the customers data file.

        Returns:
            Reservation instance or None if creation fails.
        """
        if not reservation_id or not customer_id or not hotel_id:
            print("Error: All IDs are required for a reservation.")
            return None

        customers = Customer._load_all(customer_file)
        customer_exists = any(
            c.get("customer_id") == customer_id for c in customers
        )
        if not customer_exists:
            print(f"Error: Customer with ID '{customer_id}' not found.")
            return None

        hotels = Hotel._load_all(hotel_file)
        hotel_exists = any(
            h.get("hotel_id") == hotel_id for h in hotels
        )
        if not hotel_exists:
            print(f"Error: Hotel with ID '{hotel_id}' not found.")
            return None

        reservations = cls._load_all(data_file)
        for existing in reservations:
            if existing.get("reservation_id") == reservation_id:
                print(
                    f"Error: Reservation with ID "
                    f"'{reservation_id}' already exists."
                )
                return None

        if not Hotel.reserve_room(hotel_id, hotel_file):
            return None

        reservation = cls(reservation_id, customer_id, hotel_id)
        reservations.append(reservation.to_dict())
        cls._save_all(reservations, data_file)
        return reservation

    @classmethod
    def cancel_reservation(cls, reservation_id, data_file=None,
                           hotel_file=None):
        """Cancel an existing reservation.

        Removes the reservation and returns the room to available.

        Args:
            reservation_id: ID of the reservation to cancel.
            data_file: Optional path to the reservations data file.
            hotel_file: Optional path to the hotels data file.

        Returns:
            True if cancelled, False otherwise.
        """
        reservations = cls._load_all(data_file)
        reservation_data = None
        for res in reservations:
            if res.get("reservation_id") == reservation_id:
                reservation_data = res
                break

        if reservation_data is None:
            print(
                f"Error: Reservation with ID "
                f"'{reservation_id}' not found."
            )
            return False

        hotel_id = reservation_data.get("hotel_id")
        Hotel.cancel_reservation_room(hotel_id, hotel_file)

        reservations = [
            r for r in reservations
            if r.get("reservation_id") != reservation_id
        ]
        cls._save_all(reservations, data_file)
        return True
