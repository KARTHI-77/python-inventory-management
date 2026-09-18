import json
from pathlib import Path


class InventoryManager:
    """Manage products and inventory operations."""

    def __init__(self):
        """Initialize an empty inventory."""
        self._products = {}

    def add_product(self, product_id, name, price, quantity):
        """Add a new product to the inventory."""

        if not product_id or not str(product_id).strip():
            raise ValueError("Product ID cannot be empty")

        if not name or not str(name).strip():
            raise ValueError("Product name cannot be empty")

        if price < 0:
            raise ValueError("Product price cannot be negative")

        if quantity < 0:
            raise ValueError("Product quantity cannot be negative")

        if product_id in self._products:
            raise ValueError(
                f"Product with ID '{product_id}' already exists"
            )

        self._products[product_id] = {
            "id": product_id,
            "name": name,
            "price": float(price),
            "quantity": quantity,
        }

    def remove_product(self, product_id):
        """Remove a product from the inventory."""

        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        del self._products[product_id]

    def get_product(self, product_id):
        """Return a product by its ID."""

        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        return self._products[product_id].copy()

    def list_products(self):
        """Return all products in the inventory."""

        return [
            product.copy()
            for product in self._products.values()
        ]

    def update_stock(self, product_id, quantity):
        """Update the quantity of an existing product."""

        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        if quantity < 0:
            raise ValueError("Product quantity cannot be negative")

        self._products[product_id]["quantity"] = quantity

    def search_products(self, search_term):
        """Search products by name, ignoring letter case."""

        search_term = str(search_term).strip().lower()

        return [
            product.copy()
            for product in self._products.values()
            if search_term in product["name"].lower()
        ]

    def calculate_inventory_value(self):
        """Calculate the total value of all inventory."""

        return sum(
            product["price"] * product["quantity"]
            for product in self._products.values()
        )

    def get_low_stock_products(self, threshold=5):
        """Return products whose quantity is at or below the threshold."""

        if threshold < 0:
            raise ValueError("Threshold cannot be negative")

        return [
            product.copy()
            for product in self._products.values()
            if product["quantity"] <= threshold
        ]

    def save_to_json(self, file_path):
        """Save the inventory to a JSON file."""

        file_path = Path(file_path)

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.list_products(),
                file,
                indent=4,
            )

    def load_from_json(self, file_path):
        """Load inventory data from a JSON file."""

        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as file:
            products = json.load(file)

        self._products = {}

        for product in products:
            self.add_product(
                product_id=product["id"],
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
            )