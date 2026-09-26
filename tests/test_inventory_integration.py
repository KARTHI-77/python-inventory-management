import json

import pytest

from inventory.manager import InventoryManager


def test_save_and_load_inventory(tmp_path):
    inventory = InventoryManager()

    inventory.add_product(
        "P001",
        "Keyboard",
        1200.00,
        10,
    )

    inventory.add_product(
        "P002",
        "Mouse",
        600.00,
        5,
    )

    file_path = tmp_path / "inventory.json"

    inventory.save_to_json(file_path)

    new_inventory = InventoryManager()
    new_inventory.load_from_json(file_path)

    assert new_inventory.get_product("P001") == {
        "id": "P001",
        "name": "Keyboard",
        "price": 1200.00,
        "quantity": 10,
    }

    assert new_inventory.get_product("P002") == {
        "id": "P002",
        "name": "Mouse",
        "price": 600.00,
        "quantity": 5,
    }


def test_saved_inventory_is_valid_json(tmp_path):
    inventory = InventoryManager()

    inventory.add_product(
        "P001",
        "Keyboard",
        1200.00,
        10,
    )

    file_path = tmp_path / "inventory.json"

    inventory.save_to_json(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "P001"


def test_load_missing_file_is_rejected(tmp_path):
    inventory = InventoryManager()

    missing_file = tmp_path / "does_not_exist.json"

    try:
        inventory.load_from_json(missing_file)
    except FileNotFoundError:
        assert True

def test_load_malformed_json_is_rejected(tmp_path):
    inventory = InventoryManager()

    file_path = tmp_path / "invalid.json"

    file_path.write_text(
        "{ this is not valid JSON }",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        inventory.load_from_json(file_path)

def test_load_invalid_json_structure_is_rejected(tmp_path):
    inventory = InventoryManager()

    file_path = tmp_path / "invalid_structure.json"

    file_path.write_text(
        '{"id": "P001", "name": "Keyboard"}',
        encoding="utf-8",
    )

    with pytest.raises((TypeError, KeyError)):
        inventory.load_from_json(file_path)

def test_load_invalid_product_data_is_rejected(tmp_path):
    inventory = InventoryManager()

    file_path = tmp_path / "invalid_product.json"

    file_path.write_text(
        """
        [
            {
                "id": "P001",
                "name": "Keyboard",
                "price": 1200,
                "quantity": -5
            }
        ]
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="quantity"):
        inventory.load_from_json(file_path)

def test_failed_load_does_not_modify_existing_inventory(tmp_path):
    inventory = InventoryManager()

    inventory.add_product(
        "P001",
        "Keyboard",
        1200.00,
        10,
    )

    file_path = tmp_path / "malicious_inventory.json"

    file_path.write_text(
        """
        [
            {
                "id": "P002",
                "name": "Mouse",
                "price": 600,
                "quantity": 5
            },
            {
                "id": "P003",
                "name": "Monitor",
                "price": 15000,
                "quantity": -10
            }
        ]
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="quantity"):
        inventory.load_from_json(file_path)

    assert inventory.get_product("P001") == {
        "id": "P001",
        "name": "Keyboard",
        "price": 1200.00,
        "quantity": 10,
    }