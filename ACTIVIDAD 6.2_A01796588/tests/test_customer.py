"""Unit tests for the Customer class."""
import json
import os
import tempfile
import unittest

from reservation_system.customer import Customer


class TestCustomerPositive(unittest.TestCase):
    """Positive test cases for the Customer class."""

    def setUp(self):
        """Set up temporary data file for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "customers.json")

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_customer_success(self):
        """Test successful customer creation."""
        customer = Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, "C001")
        self.assertEqual(customer.name, "Juan Perez")
        self.assertEqual(customer.email, "juan@email.com")
        self.assertEqual(customer.phone, "5551234567")

    def test_delete_customer_success(self):
        """Test successful customer deletion."""
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        result = Customer.delete_customer(
            "C001", data_file=self.data_file
        )
        self.assertTrue(result)

    def test_display_customer_info_success(self):
        """Test displaying customer information."""
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        customer = Customer.display_customer_info(
            "C001", data_file=self.data_file
        )
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Juan Perez")

    def test_modify_customer_info_success(self):
        """Test successful customer modification."""
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        updated = Customer.modify_customer_info(
            "C001", data_file=self.data_file,
            name="Juan P. Lopez", email="juan.lopez@email.com"
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Juan P. Lopez")
        self.assertEqual(updated.email, "juan.lopez@email.com")

    def test_modify_customer_phone(self):
        """Test modifying customer phone number."""
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        updated = Customer.modify_customer_info(
            "C001", data_file=self.data_file, phone="5559999999"
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated.phone, "5559999999")

    def test_to_dict(self):
        """Test converting customer to dictionary."""
        customer = Customer(
            "C001", "Test", "test@email.com", "123"
        )
        result = customer.to_dict()
        self.assertEqual(result["customer_id"], "C001")
        self.assertEqual(result["email"], "test@email.com")

    def test_from_dict_success(self):
        """Test creating customer from valid dictionary."""
        data = {
            "customer_id": "C001", "name": "Test",
            "email": "test@email.com", "phone": "123"
        }
        customer = Customer.from_dict(data)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, "C001")

    def test_load_empty_file(self):
        """Test loading when no file exists."""
        result = Customer.load_all(data_file=self.data_file)
        self.assertEqual(result, [])

    def test_create_multiple_customers(self):
        """Test creating multiple different customers."""
        Customer.create_customer(
            "C001", "Juan", "juan@mail.com", "111",
            data_file=self.data_file
        )
        Customer.create_customer(
            "C002", "Maria", "maria@mail.com", "222",
            data_file=self.data_file
        )
        customers = Customer.load_all(data_file=self.data_file)
        self.assertEqual(len(customers), 2)


class TestCustomerNegative(unittest.TestCase):
    """Negative test cases for the Customer class."""

    def setUp(self):
        """Set up temporary data file for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "customers.json")

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_customer_duplicate_id(self):
        """Negative: Create customer with duplicate ID."""
        Customer.create_customer(
            "C001", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        duplicate = Customer.create_customer(
            "C001", "Maria Lopez", "maria@email.com", "5559876543",
            data_file=self.data_file
        )
        self.assertIsNone(duplicate)

    def test_create_customer_empty_id(self):
        """Negative: Create customer with empty ID."""
        customer = Customer.create_customer(
            "", "Juan Perez", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        self.assertIsNone(customer)

    def test_create_customer_empty_name(self):
        """Negative: Create customer with empty name."""
        customer = Customer.create_customer(
            "C001", "", "juan@email.com", "5551234567",
            data_file=self.data_file
        )
        self.assertIsNone(customer)

    def test_delete_customer_not_found(self):
        """Negative: Delete a non-existent customer."""
        result = Customer.delete_customer(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertFalse(result)

    def test_display_customer_not_found(self):
        """Negative: Display a non-existent customer."""
        result = Customer.display_customer_info(
            "NONEXISTENT", data_file=self.data_file
        )
        self.assertIsNone(result)

    def test_modify_customer_not_found(self):
        """Negative: Modify a non-existent customer."""
        result = Customer.modify_customer_info(
            "NONEXISTENT", data_file=self.data_file, name="New"
        )
        self.assertIsNone(result)

    def test_from_dict_missing_field(self):
        """Negative: Create customer from dict missing field."""
        data = {"customer_id": "C001", "name": "Test"}
        customer = Customer.from_dict(data)
        self.assertIsNone(customer)

    def test_load_corrupted_json_file(self):
        """Negative: Load from a corrupted JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            file.write("corrupted json data{{")
        result = Customer.load_all(data_file=self.data_file)
        self.assertEqual(result, [])

    def test_load_invalid_format_file(self):
        """Negative: Load from file with non-list JSON."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump({"not": "a list"}, file)
        result = Customer.load_all(data_file=self.data_file)
        self.assertEqual(result, [])

    def test_create_customer_none_id(self):
        """Negative: Create customer with None as ID."""
        customer = Customer.create_customer(
            None, "Juan Perez", "juan@email.com", "555",
            data_file=self.data_file
        )
        self.assertIsNone(customer)


if __name__ == "__main__":
    unittest.main()
