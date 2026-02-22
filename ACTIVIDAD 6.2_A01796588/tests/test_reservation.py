"""Unit tests for the Reservation class."""
import json
import os
import tempfile
import unittest

from reservation_system.hotel import Hotel
from reservation_system.customer import Customer
from reservation_system.reservation import Reservation


class TestReservationPositive(unittest.TestCase):
    """Positive test cases for the Reservation class."""

    def setUp(self):
        """Set up temporary data files for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.res_file = os.path.join(
            self.temp_dir, "reservations.json"
        )
        self.hotel_file = os.path.join(
            self.temp_dir, "hotels.json"
        )
        self.cust_file = os.path.join(
            self.temp_dir, "customers.json"
        )
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.hotel_file
        )
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "555",
            data_file=self.cust_file
        )

    def tearDown(self):
        """Clean up temporary files after each test."""
        for fname in [self.res_file, self.hotel_file, self.cust_file]:
            if os.path.exists(fname):
                os.remove(fname)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_reservation_success(self):
        """Test successful reservation creation."""
        reservation = Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.reservation_id, "R001")
        self.assertEqual(reservation.customer_id, "C001")
        self.assertEqual(reservation.hotel_id, "H001")

    def test_cancel_reservation_success(self):
        """Test successful reservation cancellation."""
        Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        result = Reservation.cancel_reservation(
            "R001",
            data_file=self.res_file,
            hotel_file=self.hotel_file
        )
        self.assertTrue(result)

    def test_reservation_decreases_available_rooms(self):
        """Test that creating reservation decreases rooms."""
        Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        hotel = Hotel.display_hotel_info(
            "H001", data_file=self.hotel_file
        )
        self.assertEqual(hotel.rooms_available, 9)

    def test_cancel_reservation_restores_room(self):
        """Test that cancelling reservation restores room."""
        Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        Reservation.cancel_reservation(
            "R001",
            data_file=self.res_file,
            hotel_file=self.hotel_file
        )
        hotel = Hotel.display_hotel_info(
            "H001", data_file=self.hotel_file
        )
        self.assertEqual(hotel.rooms_available, 10)

    def test_to_dict(self):
        """Test converting reservation to dictionary."""
        reservation = Reservation("R001", "C001", "H001")
        result = reservation.to_dict()
        self.assertEqual(result["reservation_id"], "R001")
        self.assertEqual(result["customer_id"], "C001")
        self.assertEqual(result["hotel_id"], "H001")

    def test_from_dict_success(self):
        """Test creating reservation from valid dictionary."""
        data = {
            "reservation_id": "R001",
            "customer_id": "C001",
            "hotel_id": "H001"
        }
        reservation = Reservation.from_dict(data)
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.reservation_id, "R001")

    def test_load_empty_file(self):
        """Test loading when no file exists."""
        result = Reservation.load_all(data_file=self.res_file)
        self.assertEqual(result, [])

    def test_create_multiple_reservations(self):
        """Test creating multiple reservations."""
        Customer.create_customer(
            "C002", "Maria", "maria@mail.com", "222",
            data_file=self.cust_file
        )
        Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        Reservation.create_reservation(
            "R002", "C002", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        reservations = Reservation.load_all(
            data_file=self.res_file
        )
        self.assertEqual(len(reservations), 2)


class TestReservationNegative(unittest.TestCase):
    """Negative test cases for the Reservation class."""

    def setUp(self):
        """Set up temporary data files for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.res_file = os.path.join(
            self.temp_dir, "reservations.json"
        )
        self.hotel_file = os.path.join(
            self.temp_dir, "hotels.json"
        )
        self.cust_file = os.path.join(
            self.temp_dir, "customers.json"
        )
        Hotel.create_hotel(
            "H001", "Hotel Test", "Test City", 10,
            data_file=self.hotel_file
        )
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "555",
            data_file=self.cust_file
        )

    def tearDown(self):
        """Clean up temporary files after each test."""
        for fname in [self.res_file, self.hotel_file, self.cust_file]:
            if os.path.exists(fname):
                os.remove(fname)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_reservation_nonexistent_customer(self):
        """Negative: Reservation with non-existent customer."""
        reservation = Reservation.create_reservation(
            "R001", "NONEXISTENT", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(reservation)

    def test_create_reservation_nonexistent_hotel(self):
        """Negative: Reservation with non-existent hotel."""
        reservation = Reservation.create_reservation(
            "R001", "C001", "NONEXISTENT",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(reservation)

    def test_create_reservation_duplicate_id(self):
        """Negative: Create reservation with duplicate ID."""
        Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        duplicate = Reservation.create_reservation(
            "R001", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(duplicate)

    def test_create_reservation_no_rooms_available(self):
        """Negative: Reservation when no rooms available."""
        Hotel.create_hotel(
            "H002", "Small Hotel", "Town", 1,
            data_file=self.hotel_file
        )
        Reservation.create_reservation(
            "R001", "C001", "H002",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        reservation = Reservation.create_reservation(
            "R002", "C001", "H002",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(reservation)

    def test_create_reservation_empty_ids(self):
        """Negative: Create reservation with empty IDs."""
        reservation = Reservation.create_reservation(
            "", "C001", "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(reservation)

    def test_create_reservation_none_customer_id(self):
        """Negative: Reservation with None customer ID."""
        reservation = Reservation.create_reservation(
            "R001", None, "H001",
            data_file=self.res_file,
            hotel_file=self.hotel_file,
            customer_file=self.cust_file
        )
        self.assertIsNone(reservation)

    def test_cancel_reservation_not_found(self):
        """Negative: Cancel a non-existent reservation."""
        result = Reservation.cancel_reservation(
            "NONEXISTENT",
            data_file=self.res_file,
            hotel_file=self.hotel_file
        )
        self.assertFalse(result)

    def test_from_dict_missing_field(self):
        """Negative: Reservation from dict missing field."""
        data = {
            "reservation_id": "R001",
            "customer_id": "C001"
        }
        reservation = Reservation.from_dict(data)
        self.assertIsNone(reservation)

    def test_load_corrupted_json_file(self):
        """Negative: Load from a corrupted JSON file."""
        with open(self.res_file, "w", encoding="utf-8") as file:
            file.write("not valid json{{{")
        result = Reservation.load_all(data_file=self.res_file)
        self.assertEqual(result, [])

    def test_load_invalid_format_file(self):
        """Negative: Load from file with non-list JSON."""
        with open(self.res_file, "w", encoding="utf-8") as file:
            json.dump({"not": "a list"}, file)
        result = Reservation.load_all(data_file=self.res_file)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
