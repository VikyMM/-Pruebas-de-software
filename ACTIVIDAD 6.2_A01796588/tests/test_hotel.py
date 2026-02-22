"""Unit tests for the Hotel class."""
import json
import os
import tempfile
import unittest

from reservation_system.hotel import Hotel


class TestHotelPositive(unittest.TestCase):
    """Positive test cases for the Hotel class."""

    def setUp(self):
        """Set up temporary data file for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "hotels.json")

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_hotel_success(self):
        """Test successful hotel creation."""
        hotel = Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, "H001")
        self.assertEqual(hotel.name, "Hotel Test")
        self.assertEqual(hotel.location, "Test City")
        self.assertEqual(hotel.total_rooms, 10)
        self.assertEqual(hotel.rooms_available, 10)

    def test_delete_hotel_success(self):
        """Test successful hotel deletion."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        result = Hotel.delete_hotel("H001", data_file=self.data_file)
        self.assertTrue(result)

    def test_display_hotel_info_success(self):
        """Test displaying hotel information."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        hotel = Hotel.display_hotel_info(
            "H001", data_file=self.data_file
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Hotel Test")

    def test_modify_hotel_info_success(self):
        """Test successful hotel modification."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        updated = Hotel.modify_hotel_info(
            "H001", data_file=self.data_file,
            name="Hotel Updated", location="New City"
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Hotel Updated")
        self.assertEqual(updated.location, "New City")

    def test_modify_hotel_total_rooms(self):
        """Test modifying total rooms adjusts available rooms."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        Hotel.reserve_room("H001", data_file=self.data_file)
        updated = Hotel.modify_hotel_info(
            "H001", data_file=self.data_file, total_rooms=15
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.total_rooms, 15)
        self.assertEqual(updated.rooms_available, 14)

    def test_reserve_room_success(self):
        """Test successful room reservation."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        result = Hotel.reserve_room("H001", data_file=self.data_file)
        self.assertTrue(result)
        hotel = Hotel.display_hotel_info(
            "H001", data_file=self.data_file
        )
        self.assertEqual(hotel.rooms_available, 9)

    def test_cancel_reservation_room_success(self):
        """Test successful room reservation cancellation."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        Hotel.reserve_room("H001", data_file=self.data_file)
        result = Hotel.cancel_reservation_room(
            "H001", data_file=self.data_file
        )
        self.assertTrue(result)
        hotel = Hotel.display_hotel_info(
            "H001", data_file=self.data_file
        )
        self.assertEqual(hotel.rooms_available, 10)

    def test_to_dict(self):
        """Test converting hotel to dictionary."""
        hotel = Hotel("H001", "Test", "City", 5)
        result = hotel.to_dict()
        self.assertEqual(result["hotel_id"], "H001")
        self.assertEqual(result["total_rooms"], 5)

    def test_from_dict_success(self):
        """Test creating hotel from valid dictionary."""
        data = {
            "hotel_id": "H001", "name": "Test",
            "location": "City", "total_rooms": 5,
            "rooms_available": 3
        }
        hotel = Hotel.from_dict(data)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.rooms_available, 3)

    def test_load_empty_file(self):
        """Test loading when no file exists."""
        result = Hotel.load_all(data_file=self.data_file)
        self.assertEqual(result, [])


class TestHotelNegative(unittest.TestCase):
    """Negative test cases for the Hotel class."""

    def setUp(self):
        """Set up temporary data file for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "hotels.json")

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_hotel_duplicate_id(self):
        """Negative: Create hotel with duplicate ID."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        duplicate = Hotel.create_hotel(
            "H001", "Hotel Duplicate", "Other City", 5,
            data_file=self.data_file
        )
        self.assertIsNone(duplicate)

    def test_create_hotel_negative_rooms(self):
        """Negative: Create hotel with negative room count."""
        hotel = Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", -5,
            data_file=self.data_file
        )
        self.assertIsNone(hotel)

    def test_create_hotel_invalid_rooms_type(self):
        """Negative: Create hotel with non-integer room count."""
        hotel = Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", "ten",
            data_file=self.data_file
        )
        self.assertIsNone(hotel)

    def test_create_hotel_empty_id(self):
        """Negative: Create hotel with empty ID."""
        hotel = Hotel.create_hotel(
            "", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        self.assertIsNone(hotel)

    def test_create_hotel_empty_name(self):
        """Negative: Create hotel with empty name."""
        hotel = Hotel.create_hotel(
            "H001", "", "Test City", 10,
            data_file=self.data_file
        )
        self.assertIsNone(hotel)

    def test_delete_hotel_not_found(self):
        """Negative: Delete a non-existent hotel."""
        result = Hotel.delete_hotel(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertFalse(result)

    def test_display_hotel_not_found(self):
        """Negative: Display a non-existent hotel."""
        result = Hotel.display_hotel_info(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertIsNone(result)

    def test_modify_hotel_not_found(self):
        """Negative: Modify a non-existent hotel."""
        result = Hotel.modify_hotel_info(
            "NONEXISTENT", data_file=self.data_file, name="New"
        )
        self.assertIsNone(result)

    def test_modify_hotel_invalid_total_rooms(self):
        """Negative: Modify hotel with invalid total_rooms."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        result = Hotel.modify_hotel_info(
            "H001", data_file=self.data_file, total_rooms=-1
        )
        self.assertIsNone(result)

    def test_reserve_room_no_availability(self):
        """Negative: Reserve room when no rooms available."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 1,
            data_file=self.data_file
        )
        Hotel.reserve_room("H001", data_file=self.data_file)
        result = Hotel.reserve_room("H001", data_file=self.data_file)
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        """Negative: Reserve room in non-existent hotel."""
        result = Hotel.reserve_room(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertFalse(result)

    def test_cancel_reservation_all_rooms_available(self):
        """Negative: Cancel when all rooms available."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 5,
            data_file=self.data_file
        )
        result = Hotel.cancel_reservation_room(
            "H001", data_file=self.data_file
        )
        self.assertFalse(result)

    def test_cancel_reservation_hotel_not_found(self):
        """Negative: Cancel for non-existent hotel."""
        result = Hotel.cancel_reservation_room(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertFalse(result)

    def test_from_dict_missing_field(self):
        """Negative: Create hotel from dict with missing field."""
        data = {"hotel_id": "H001", "name": "Test"}
        hotel = Hotel.from_dict(data)
        self.assertIsNone(hotel)

    def test_from_dict_invalid_total_rooms(self):
        """Negative: Create hotel from dict with invalid rooms."""
        data = {
            "hotel_id": "H001", "name": "Test",
            "location": "City", "total_rooms": -1
        }
        hotel = Hotel.from_dict(data)
        self.assertIsNone(hotel)

    def test_load_corrupted_json_file(self):
        """Negative: Load from a corrupted JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            file.write("not valid json{{{")
        result = Hotel.load_all(data_file=self.data_file)
        self.assertEqual(result, [])

    def test_load_invalid_format_file(self):
        """Negative: Load from file with non-list JSON."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump({"key": "value"}, file)
        result = Hotel.load_all(data_file=self.data_file)
        self.assertEqual(result, [])

    def test_modify_hotel_total_rooms_string(self):
        """Negative: Modify total_rooms with a string value."""
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.data_file
        )
        result = Hotel.modify_hotel_info(
            "H001", data_file=self.data_file, total_rooms="five"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
