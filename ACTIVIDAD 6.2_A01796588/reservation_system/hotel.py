"""Module for Hotel class with persistent storage."""
import os

from reservation_system.file_utils import load_json_list, save_json_list


class Hotel:
    """Represents a hotel with rooms and persistent file storage."""

    DATA_FILE = os.path.join("data", "hotels.json")

    def __init__(self, hotel_id, name, location, total_rooms):
        """Initialize a Hotel instance.

        Args:
            hotel_id: Unique identifier for the hotel.
            name: Name of the hotel.
            location: Location/address of the hotel.
            total_rooms: Total number of rooms available.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.rooms_available = total_rooms

    def to_dict(self):
        """Convert hotel instance to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "rooms_available": self.rooms_available,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Hotel instance from a dictionary.

        Args:
            data: Dictionary with hotel attributes.

        Returns:
            Hotel instance or None if data is invalid.
        """
        try:
            required = ["hotel_id", "name", "location", "total_rooms"]
            for field in required:
                if field not in data:
                    print(
                        f"Error: Missing field '{field}' in hotel data."
                    )
                    return None
            if not isinstance(data["total_rooms"], int) or \
                    data["total_rooms"] < 0:
                print(
                    "Error: 'total_rooms' must be a non-negative integer."
                )
                return None
            hotel = cls(
                data["hotel_id"],
                data["name"],
                data["location"],
                data["total_rooms"],
            )
            if "rooms_available" in data:
                rooms_avail = data["rooms_available"]
                if isinstance(rooms_avail, int) and \
                        0 <= rooms_avail <= data["total_rooms"]:
                    hotel.rooms_available = rooms_avail
            return hotel
        except (TypeError, KeyError) as exc:
            print(f"Error creating hotel from data: {exc}")
            return None

    @staticmethod
    def load_all(data_file=None):
        """Load all hotels from the JSON file.

        Args:
            data_file: Optional path to the data file.

        Returns:
            List of hotel dictionaries.
        """
        file_path = data_file or Hotel.DATA_FILE
        return load_json_list(file_path, "hotel")

    @staticmethod
    def save_all(hotels, data_file=None):
        """Save all hotels to the JSON file.

        Args:
            hotels: List of hotel dictionaries to save.
            data_file: Optional path to the data file.
        """
        file_path = data_file or Hotel.DATA_FILE
        save_json_list(hotels, file_path)

    @classmethod
    def create_hotel(  # pylint: disable=too-many-arguments
            cls, hotel_id, name, location,
            total_rooms, *, data_file=None):
        """Create a new hotel and save it to the data file.

        Args:
            hotel_id: Unique identifier for the hotel.
            name: Name of the hotel.
            location: Location of the hotel.
            total_rooms: Total number of rooms.
            data_file: Optional path to the data file.

        Returns:
            Hotel instance or None if creation fails.
        """
        if not isinstance(total_rooms, int) or total_rooms < 0:
            print("Error: 'total_rooms' must be a non-negative integer.")
            return None
        if not hotel_id or not name:
            print("Error: 'hotel_id' and 'name' are required.")
            return None
        hotels = cls.load_all(data_file)
        for existing in hotels:
            if existing.get("hotel_id") == hotel_id:
                print(
                    f"Error: Hotel with ID '{hotel_id}' already exists."
                )
                return None
        hotel = cls(hotel_id, name, location, total_rooms)
        hotels.append(hotel.to_dict())
        cls.save_all(hotels, data_file)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id, data_file=None):
        """Delete a hotel from the data file.

        Args:
            hotel_id: ID of the hotel to delete.
            data_file: Optional path to the data file.

        Returns:
            True if deleted, False otherwise.
        """
        hotels = cls.load_all(data_file)
        original_count = len(hotels)
        hotels = [h for h in hotels if h.get("hotel_id") != hotel_id]
        if len(hotels) == original_count:
            print(f"Error: Hotel with ID '{hotel_id}' not found.")
            return False
        cls.save_all(hotels, data_file)
        return True

    @classmethod
    def display_hotel_info(cls, hotel_id, data_file=None):
        """Display information of a specific hotel.

        Args:
            hotel_id: ID of the hotel to display.
            data_file: Optional path to the data file.

        Returns:
            Hotel instance or None if not found.
        """
        hotels = cls.load_all(data_file)
        for hotel_data in hotels:
            if hotel_data.get("hotel_id") == hotel_id:
                hotel = cls.from_dict(hotel_data)
                if hotel:
                    print(f"Hotel ID: {hotel.hotel_id}")
                    print(f"Name: {hotel.name}")
                    print(f"Location: {hotel.location}")
                    print(f"Total Rooms: {hotel.total_rooms}")
                    print(f"Rooms Available: {hotel.rooms_available}")
                return hotel
        print(f"Error: Hotel with ID '{hotel_id}' not found.")
        return None

    @classmethod
    def modify_hotel_info(cls, hotel_id, data_file=None, **kwargs):
        """Modify hotel information.

        Args:
            hotel_id: ID of the hotel to modify.
            data_file: Optional path to the data file.
            **kwargs: Fields to update (name, location, total_rooms).

        Returns:
            Updated Hotel instance or None if not found.
        """
        hotels = cls.load_all(data_file)
        for i, hotel_data in enumerate(hotels):
            if hotel_data.get("hotel_id") == hotel_id:
                if "name" in kwargs:
                    hotels[i]["name"] = kwargs["name"]
                if "location" in kwargs:
                    hotels[i]["location"] = kwargs["location"]
                if "total_rooms" in kwargs:
                    new_total = kwargs["total_rooms"]
                    if not isinstance(new_total, int) or new_total < 0:
                        print(
                            "Error: 'total_rooms' must be non-negative."
                        )
                        return None
                    old_total = hotels[i]["total_rooms"]
                    old_avail = hotels[i].get(
                        "rooms_available", old_total
                    )
                    diff = new_total - old_total
                    new_avail = max(0, old_avail + diff)
                    hotels[i]["total_rooms"] = new_total
                    hotels[i]["rooms_available"] = min(
                        new_avail, new_total
                    )
                cls.save_all(hotels, data_file)
                return cls.from_dict(hotels[i])
        print(f"Error: Hotel with ID '{hotel_id}' not found.")
        return None

    @classmethod
    def reserve_room(cls, hotel_id, data_file=None):
        """Reserve a room in the specified hotel.

        Args:
            hotel_id: ID of the hotel.
            data_file: Optional path to the data file.

        Returns:
            True if room reserved, False otherwise.
        """
        hotels = cls.load_all(data_file)
        for i, hotel_data in enumerate(hotels):
            if hotel_data.get("hotel_id") == hotel_id:
                available = hotel_data.get("rooms_available", 0)
                if available <= 0:
                    print("Error: No rooms available.")
                    return False
                hotels[i]["rooms_available"] = available - 1
                cls.save_all(hotels, data_file)
                return True
        print(f"Error: Hotel with ID '{hotel_id}' not found.")
        return False

    @classmethod
    def cancel_reservation_room(cls, hotel_id, data_file=None):
        """Cancel a room reservation, returning room to available.

        Args:
            hotel_id: ID of the hotel.
            data_file: Optional path to the data file.

        Returns:
            True if cancellation successful, False otherwise.
        """
        hotels = cls.load_all(data_file)
        for i, hotel_data in enumerate(hotels):
            if hotel_data.get("hotel_id") == hotel_id:
                available = hotel_data.get("rooms_available", 0)
                total = hotel_data.get("total_rooms", 0)
                if available >= total:
                    print("Error: All rooms are already available.")
                    return False
                hotels[i]["rooms_available"] = available + 1
                cls.save_all(hotels, data_file)
                return True
        print(f"Error: Hotel with ID '{hotel_id}' not found.")
        return False
