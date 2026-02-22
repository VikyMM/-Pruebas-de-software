"""Module for Customer class with persistent storage."""
import json
import os


class Customer:
    """Represents a customer with persistent file storage."""

    DATA_FILE = os.path.join("data", "customers.json")

    def __init__(self, customer_id, name, email, phone):
        """Initialize a Customer instance.

        Args:
            customer_id: Unique identifier for the customer.
            name: Full name of the customer.
            email: Email address of the customer.
            phone: Phone number of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convert customer instance to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Customer instance from a dictionary.

        Args:
            data: Dictionary with customer attributes.

        Returns:
            Customer instance or None if data is invalid.
        """
        try:
            required = ["customer_id", "name", "email", "phone"]
            for field in required:
                if field not in data:
                    print(f"Error: Missing field '{field}' in customer data.")
                    return None
            return cls(
                data["customer_id"],
                data["name"],
                data["email"],
                data["phone"],
            )
        except (TypeError, KeyError) as exc:
            print(f"Error creating customer from data: {exc}")
            return None

    @staticmethod
    def _load_all(data_file=None):
        """Load all customers from the JSON file.

        Args:
            data_file: Optional path to the data file.

        Returns:
            List of customer dictionaries.
        """
        file_path = data_file or Customer.DATA_FILE
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    print("Error: Customer data file has invalid format.")
                    return []
                return data
        except json.JSONDecodeError as exc:
            print(f"Error reading customer data file: {exc}")
            return []
        except OSError as exc:
            print(f"Error accessing customer data file: {exc}")
            return []

    @staticmethod
    def _save_all(customers, data_file=None):
        """Save all customers to the JSON file.

        Args:
            customers: List of customer dictionaries to save.
            data_file: Optional path to the data file.
        """
        file_path = data_file or Customer.DATA_FILE
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(customers, file, indent=2)

    @classmethod
    def create_customer(cls, customer_id, name, email, phone,
                        data_file=None):
        """Create a new customer and save to the data file.

        Args:
            customer_id: Unique identifier for the customer.
            name: Full name of the customer.
            email: Email address.
            phone: Phone number.
            data_file: Optional path to the data file.

        Returns:
            Customer instance or None if creation fails.
        """
        if not customer_id or not name:
            print("Error: 'customer_id' and 'name' are required.")
            return None
        customers = cls._load_all(data_file)
        for existing in customers:
            if existing.get("customer_id") == customer_id:
                print(
                    f"Error: Customer with ID '{customer_id}' already exists."
                )
                return None
        customer = cls(customer_id, name, email, phone)
        customers.append(customer.to_dict())
        cls._save_all(customers, data_file)
        return customer

    @classmethod
    def delete_customer(cls, customer_id, data_file=None):
        """Delete a customer from the data file.

        Args:
            customer_id: ID of the customer to delete.
            data_file: Optional path to the data file.

        Returns:
            True if deleted, False otherwise.
        """
        customers = cls._load_all(data_file)
        original_count = len(customers)
        customers = [
            c for c in customers if c.get("customer_id") != customer_id
        ]
        if len(customers) == original_count:
            print(f"Error: Customer with ID '{customer_id}' not found.")
            return False
        cls._save_all(customers, data_file)
        return True

    @classmethod
    def display_customer_info(cls, customer_id, data_file=None):
        """Display information of a specific customer.

        Args:
            customer_id: ID of the customer to display.
            data_file: Optional path to the data file.

        Returns:
            Customer instance or None if not found.
        """
        customers = cls._load_all(data_file)
        for cust_data in customers:
            if cust_data.get("customer_id") == customer_id:
                customer = cls.from_dict(cust_data)
                if customer:
                    print(f"Customer ID: {customer.customer_id}")
                    print(f"Name: {customer.name}")
                    print(f"Email: {customer.email}")
                    print(f"Phone: {customer.phone}")
                return customer
        print(f"Error: Customer with ID '{customer_id}' not found.")
        return None

    @classmethod
    def modify_customer_info(cls, customer_id, data_file=None, **kwargs):
        """Modify customer information.

        Args:
            customer_id: ID of the customer to modify.
            data_file: Optional path to the data file.
            **kwargs: Fields to update (name, email, phone).

        Returns:
            Updated Customer instance or None if not found.
        """
        customers = cls._load_all(data_file)
        for i, cust_data in enumerate(customers):
            if cust_data.get("customer_id") == customer_id:
                if "name" in kwargs:
                    customers[i]["name"] = kwargs["name"]
                if "email" in kwargs:
                    customers[i]["email"] = kwargs["email"]
                if "phone" in kwargs:
                    customers[i]["phone"] = kwargs["phone"]
                cls._save_all(customers, data_file)
                return cls.from_dict(customers[i])
        print(f"Error: Customer with ID '{customer_id}' not found.")
        return None
