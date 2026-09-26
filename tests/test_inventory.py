import pytest

from inventory.manager import InventoryManager


class TestInventoryManager:

    def test_inventory_starts_empty(self):
        inventory = InventoryManager()

        assert inventory.list_products() == []

    def test_add_product(self):
        inventory = InventoryManager()

        inventory.add_product(
            product_id="P001",
            name="Keyboard",
            price=1200.00,
            quantity=10,
        )

        product = inventory.get_product("P001")

        assert product["id"] == "P001"
        assert product["name"] == "Keyboard"
        assert product["price"] == 1200.00
        assert product["quantity"] == 10

    def test_add_multiple_products(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)
        inventory.add_product("P002", "Mouse", 600.00, 5)

        products = inventory.list_products()

        assert len(products) == 2

    def test_duplicate_product_id_is_rejected(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        with pytest.raises(ValueError, match="already exists"):
            inventory.add_product("P001", "Mouse", 600.00, 5)

    def test_negative_price_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(ValueError, match="price"):
            inventory.add_product("P001", "Keyboard", -100.00, 10)

    def test_negative_quantity_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(ValueError, match="quantity"):
            inventory.add_product("P001", "Keyboard", 1200.00, -5)

    def test_empty_product_name_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(ValueError, match="name"):
            inventory.add_product("P001", "", 1200.00, 10)

    def test_empty_product_id_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(ValueError, match="Product ID"):
            inventory.add_product("", "Keyboard", 1200.00, 10)

    def test_whitespace_product_id_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(ValueError, match="Product ID"):
            inventory.add_product("   ", "Keyboard", 1200.00, 10)

    def test_remove_product(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        inventory.remove_product("P001")

        assert inventory.list_products() == []

    def test_remove_nonexistent_product_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(KeyError, match="not found"):
            inventory.remove_product("P999")

    def test_update_stock(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        inventory.update_stock("P001", 15)

        product = inventory.get_product("P001")

        assert product["quantity"] == 15

    def test_stock_can_be_updated_to_zero(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        inventory.update_stock("P001", 0)

        product = inventory.get_product("P001")

        assert product["quantity"] == 0

    def test_negative_stock_is_rejected(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        with pytest.raises(ValueError, match="quantity"):
            inventory.update_stock("P001", -1)

    def test_update_nonexistent_product_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(KeyError, match="not found"):
            inventory.update_stock("P999", 10)

    def test_get_nonexistent_product_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises(KeyError, match="not found"):
            inventory.get_product("P999")

    def test_search_products_by_name(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Mechanical Keyboard", 2500.00, 10)
        inventory.add_product("P002", "Wireless Mouse", 800.00, 5)

        results = inventory.search_products("keyboard")

        assert len(results) == 1
        assert results[0]["id"] == "P001"

    def test_search_is_case_insensitive(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Mechanical Keyboard", 2500.00, 10)

        results = inventory.search_products("KEYBOARD")

        assert len(results) == 1

    def test_search_with_no_match_returns_empty_list(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        results = inventory.search_products("Monitor")

        assert results == []

    def test_calculate_inventory_value(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)
        inventory.add_product("P002", "Mouse", 600.00, 5)

        total = inventory.calculate_inventory_value()

        assert total == 15000.00

    def test_empty_inventory_has_zero_value(self):
        inventory = InventoryManager()

        assert inventory.calculate_inventory_value() == 0.0

    def test_get_low_stock_products(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)
        inventory.add_product("P002", "Mouse", 600.00, 3)
        inventory.add_product("P003", "Monitor", 8000.00, 1)

        low_stock = inventory.get_low_stock_products(threshold=5)

        ids = {product["id"] for product in low_stock}

        assert ids == {"P002", "P003"}

    def test_no_low_stock_products_returns_empty_list(self):
        inventory = InventoryManager()

        inventory.add_product("P001", "Keyboard", 1200.00, 10)

        assert inventory.get_low_stock_products(threshold=5) == []

    def test_negative_low_stock_threshold_is_rejected(self):
        inventory = InventoryManager()

        inventory.add_product(
            "P001",
            "Keyboard",
            1200.00,
            10,
        )

        with pytest.raises(ValueError, match="Threshold"):
            inventory.get_low_stock_products(threshold=-1)

    def test_non_numeric_price_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises((TypeError, ValueError)):
            inventory.add_product(
                "P001",
                "Keyboard",
                "free",
                10,
            )

    def test_non_integer_quantity_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises((TypeError, ValueError)):
            inventory.add_product(
                "P001",
                "Keyboard",
                1200.00,
                "ten",
            )

    def test_non_integer_stock_update_is_rejected(self):
        inventory = InventoryManager()

        inventory.add_product(
            "P001",
            "Keyboard",
            1200.00,
            10,
        )

        with pytest.raises((TypeError, ValueError)):
            inventory.update_stock("P001", "ten")

    def test_non_integer_low_stock_threshold_is_rejected(self):
        inventory = InventoryManager()

        with pytest.raises((TypeError, ValueError)):
            inventory.get_low_stock_products("five")


def test_nan_price_is_rejected():
    inventory = InventoryManager()

    with pytest.raises(ValueError, match="finite"):
        inventory.add_product(
            "P001",
            "Keyboard",
            float("nan"),
            10,
        )


def test_infinite_price_is_rejected():
    inventory = InventoryManager()

    with pytest.raises(ValueError, match="finite"):
        inventory.add_product(
            "P001",
            "Keyboard",
            float("inf"),
            10,
        )