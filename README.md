# Python Inventory Management

A Python inventory management module designed to demonstrate clean Python development and comprehensive automated testing using pytest.

## Overview

This project provides a simple inventory management system for adding, removing, updating, searching, and managing products.

The project is being developed as part of a Python development internship task, with a focus on automated testing, edge-case handling, integration testing, and maintainable Python code.

## Features

- Add products to inventory
- Remove products from inventory
- Retrieve product information
- List all products
- Update product stock
- Search products by name
- Identify low-stock products
- Calculate total inventory value
- Save inventory data to JSON
- Load inventory data from JSON
- Validate invalid product and inventory data

## Technologies Used

- Python
- pytest
- pytest-cov
- JSON
- Git & GitHub

## Project Structure

```text
python-inventory-management/
│
├── inventory/
│   ├── __init__.py
│   └── manager.py
│
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py
│   └── test_inventory_integration.py
│
├── .gitignore
├── README.md
├── pytest.ini
└── requirements.txt