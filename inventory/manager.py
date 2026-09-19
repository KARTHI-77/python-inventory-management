import json
from pathlib import Path
from typing import Any


Product = dict[str, Any]


class InventoryManager:
    """Manage products and inventory operations."""

    def __init__(self) -> None:
        """Initialize an empty inventory."""
        self._products: dict[str, Product] = {}

    @staticmethod
    def _validate_product_id(product_id: str) -> None:
        """Validate a product ID.

        Args:
            product_id: Unique identifier for a product.

        Raises:
            ValueError: If the product ID is empty or contains only whitespace.
        """
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty")

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate a product name.

        Args:
            name: Name of the product.

        Raises:
            ValueError: If the product name is empty or contains only whitespace.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty")

    @staticmethod
    def _validate_price(price: float) -> None:
        """Validate a product price.

        Args:
            price: Product price.

        Raises:
            TypeError: If price is not numeric.
            ValueError: If price is negative.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("Product price must be numeric")

        if price < 0:
            raise ValueError("Product price cannot be negative")

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        """Validate a product quantity.

        Args:
            quantity: Number of units in stock.

        Raises:
            TypeError: If quantity is not an integer.
            ValueError: If quantity is negative.
        """
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Product quantity must be an integer")

        if quantity < 0:
            raise ValueError("Product quantity cannot be negative")

    def add_product(
        self,
        product_id: str,
        name: str,
        price: float,
        quantity: int,
    ) -> None:
        """Add a new product to the inventory.

        Args:
            product_id: Unique product identifier.
            name: Product name.
            price: Product price.
            quantity: Initial stock quantity.

        Raises:
            ValueError: If product data is invalid or the ID already exists.
            TypeError: If price or quantity has an invalid type.
        """
        self._validate_product_id(product_id)
        self._validate_name(name)
        self._validate_price(price)
        self._validate_quantity(quantity)

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

    def remove_product(self, product_id: str) -> None:
        """Remove a product from the inventory.

        Args:
            product_id: ID of the product to remove.

        Raises:
            KeyError: If the product does not exist.
        """
        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        del self._products[product_id]

    def get_product(self, product_id: str) -> Product:
        """Return a copy of a product by its ID.

        Args:
            product_id: ID of the product to retrieve.

        Returns:
            A copy of the requested product.

        Raises:
            KeyError: If the product does not exist.
        """
        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        return self._products[product_id].copy()

    def list_products(self) -> list[Product]:
        """Return copies of all products in the inventory."""
        return [product.copy() for product in self._products.values()]

    def update_stock(
        self,
        product_id: str,
        quantity: int,
    ) -> None:
        """Update the quantity of an existing product.

        Args:
            product_id: ID of the product to update.
            quantity: New stock quantity.

        Raises:
            KeyError: If the product does not exist.
            TypeError: If quantity is not an integer.
            ValueError: If quantity is negative.
        """
        if product_id not in self._products:
            raise KeyError(f"Product '{product_id}' not found")

        self._validate_quantity(quantity)
        self._products[product_id]["quantity"] = quantity

    def search_products(self, search_term: str) -> list[Product]:
        """Search products by name, ignoring letter case.

        Args:
            search_term: Text to search for in product names.

        Returns:
            A list of matching products.
        """
        search_term = str(search_term).strip().lower()

        return [
            product.copy()
            for product in self._products.values()
            if search_term in product["name"].lower()
        ]

    def calculate_inventory_value(self) -> float:
        """Calculate the total monetary value of all inventory."""
        return sum(
            product["price"] * product["quantity"]
            for product in self._products.values()
        )

    def get_low_stock_products(
        self,
        threshold: int = 5,
    ) -> list[Product]:
        """Return products at or below the stock threshold.

        Args:
            threshold: Maximum quantity considered low stock.

        Returns:
            Products whose quantity is less than or equal to the threshold.

        Raises:
            TypeError: If threshold is not an integer.
            ValueError: If threshold is negative.
        """
        if not isinstance(threshold, int) or isinstance(threshold, bool):
            raise TypeError("Threshold must be an integer")

        if threshold < 0:
            raise ValueError("Threshold cannot be negative")

        return [
            product.copy()
            for product in self._products.values()
            if product["quantity"] <= threshold
        ]

    def save_to_json(self, file_path: str | Path) -> None:
        """Save the inventory to a JSON file.

        Args:
            file_path: Destination JSON file path.
        """
        file_path = Path(file_path)

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.list_products(),
                file,
                indent=4,
            )

    def load_from_json(self, file_path: str | Path) -> None:
        """Load inventory data from a JSON file.

        Args:
            file_path: Source JSON file path.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            KeyError: If required product fields are missing.
            TypeError: If product data has an invalid type.
            ValueError: If product data contains invalid values.
        """
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