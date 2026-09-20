# Python Inventory Management

[![Python Tests](https://github.com/KARTHI-77/python-inventory-management/actions/workflows/tests.yml/badge.svg)](https://github.com/KARTHI-77/python-inventory-management/actions/workflows/tests.yml)

A Python-based inventory management module developed with a strong focus on **automated testing, Test-Driven Development (TDD), input validation, code quality, and integration testing**.

This project was developed as part of a Python programming internship to demonstrate practical Python development and professional software testing practices.

---

## 📌 Project Overview

The Python Inventory Management system provides a simple and reusable module for managing products and their stock information.

The system allows users to:

- Add products
- Remove products
- Retrieve product information
- List all products
- Update stock quantities
- Search products by name
- Calculate total inventory value
- Identify low-stock products
- Save inventory data to a JSON file
- Load inventory data from a JSON file

The project also includes a comprehensive automated test suite using **pytest**.

The implementation follows a **Test-Driven Development (TDD)** workflow where tests were written before implementing the corresponding functionality.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Build a clean and reusable Python inventory management module.
2. Apply object-oriented programming concepts.
3. Validate user and product input properly.
4. Develop automated unit tests using pytest.
5. Develop integration tests for JSON persistence.
6. Follow a Test-Driven Development workflow.
7. Handle invalid and edge-case inputs.
8. Measure and improve code coverage.
9. Maintain clean and readable Python code.
10. Use Git and GitHub for version control and project management.

---

## ✨ Features

### Product Management

- Add new products
- Prevent duplicate product IDs
- Remove products
- Retrieve individual products
- List all products
- Update product stock quantities

### Product Search

- Search products by name
- Case-insensitive searching
- Partial name matching

### Inventory Analysis

- Calculate total inventory value
- Identify products with low stock
- Configurable low-stock threshold

### Data Validation

The system validates:

- Empty product IDs
- Whitespace-only product IDs
- Empty product names
- Negative prices
- Negative quantities
- Non-numeric prices
- Non-integer quantities
- Negative stock thresholds
- Invalid stock updates
- Duplicate product IDs

### JSON Persistence

Inventory data can be:

- Saved to a JSON file
- Loaded from a JSON file

The system also handles:

- Missing JSON files
- Malformed JSON
- Invalid JSON structures
- Invalid product data

---

## ⚙️ Technologies Used

### Programming Language

- Python 3

### Testing

- pytest
- pytest-cov

### Data Storage

- JSON

### Development Tools

- Git
- GitHub
- Visual Studio Code
- Python Virtual Environment

---

## 📦 Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/KARTHI-77/python-inventory-management.git
```

### 2. Navigate to the Project Directory

```bash
cd python-inventory-management
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\activate
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 6. Verify the Installation

Check that pytest is installed:

```bash
pytest --version
```

You should see the installed pytest version.

---

## ▶️ Running the Project

The project is currently implemented as a reusable Python module rather than a standalone command-line application.

The `InventoryManager` class can be imported and used directly from Python.

### Example

Create a Python file named:

```text
example.py
```

Add the following code:

```python
from inventory.manager import InventoryManager


inventory = InventoryManager()

# Add products
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

# Display all products
print("Products:")
print(inventory.list_products())

# Search for a product
print("\nSearch Results:")
print(inventory.search_products("keyboard"))

# Update stock
inventory.update_stock("P001", 15)

# Calculate inventory value
print("\nInventory Value:")
print(inventory.calculate_inventory_value())

# Find low-stock products
print("\nLow Stock Products:")
print(inventory.get_low_stock_products(threshold=5))
```

Run the example:

```bash
python example.py
```

---

## 🧪 Running the Tests

### Run the Complete Test Suite

```bash
pytest
```

### Run Tests with Detailed Output

```bash
pytest -v
```

### Run Unit Tests Only

```bash
pytest tests/test_inventory.py -v
```

### Run Integration Tests Only

```bash
pytest tests/test_inventory_integration.py -v
```

### Run Tests with Code Coverage

```bash
pytest --cov=inventory --cov-report=term-missing
```

### Generate an HTML Coverage Report

```bash
pytest --cov=inventory --cov-report=html
```

The HTML coverage report will be generated in:

```text
htmlcov/
```

Open the following file in a browser:

```text
htmlcov/index.html
```

---

## 📊 Current Test Results

The current implementation contains:

```text
34 tests collected
34 tests passed
0 tests failed
100% code coverage
```

Current coverage:

```text
Name                    Stmts   Miss  Cover
-------------------------------------------
inventory/__init__.py       0      0   100%
inventory/manager.py       72      0   100%
-------------------------------------------
TOTAL                      72      0   100%
```

The project currently has:

- **28 unit tests**
- **6 integration tests**
- **34 total automated tests**
- **100% coverage of the inventory module**

> Code coverage measures which executable statements are executed by tests. It does not by itself guarantee that software contains no defects.

---

## 🔬 Unit Testing

Unit tests are located in:

```text
tests/test_inventory.py
```

The unit test suite verifies individual inventory operations and validation rules.

The tests cover:

- Empty inventory behavior
- Adding products
- Adding multiple products
- Duplicate product IDs
- Removing products
- Removing nonexistent products
- Retrieving products
- Updating stock
- Zero stock
- Negative stock
- Searching products
- Case-insensitive searching
- Search with no matching products
- Inventory value calculation
- Empty inventory value
- Low-stock detection
- No low-stock products
- Invalid low-stock thresholds
- Invalid price values
- Invalid quantity values
- Invalid stock updates
- Invalid product IDs
- Invalid product names

The unit test suite currently contains **28 tests**.

---

## 🔗 Integration Testing

Integration tests are located in:

```text
tests/test_inventory_integration.py
```

These tests verify the interaction between the inventory manager and the JSON persistence layer.

The integration tests cover:

- Saving inventory to JSON
- Loading inventory from JSON
- Saving and loading inventory together
- Verifying saved JSON structure
- Missing JSON files
- Malformed JSON
- Invalid JSON structures
- Invalid product data

The integration test suite currently contains **6 tests**.

---
## 🧾 Detailed Test Case Documentation

The automated test suite contains 34 test cases covering normal operations, validation
rules, edge cases, and JSON persistence.

### Unit Test Cases

| # | Test Case | Purpose |
|---:|---|---|
| 1 | Inventory starts empty | Verifies a newly created inventory contains no products. |
| 2 | Add product | Verifies that a valid product can be added successfully. |
| 3 | Add multiple products | Verifies that multiple unique products can coexist. |
| 4 | Duplicate product ID | Ensures duplicate IDs are rejected to maintain uniqueness. |
| 5 | Negative price | Ensures products cannot have negative prices. |
| 6 | Negative quantity | Ensures products cannot have negative stock. |
| 7 | Empty product name | Ensures products require a valid name. |
| 8 | Empty product ID | Ensures a product ID cannot be empty. |
| 9 | Whitespace product ID | Ensures whitespace-only IDs are rejected. |
| 10 | Remove product | Verifies an existing product can be removed. |
| 11 | Remove nonexistent product | Verifies an appropriate error is raised for an unknown product. |
| 12 | Update stock | Verifies stock quantity can be updated. |
| 13 | Update stock to zero | Ensures zero stock is accepted as a valid quantity. |
| 14 | Negative stock update | Ensures stock cannot be updated to a negative value. |
| 15 | Update nonexistent product | Verifies updating an unknown product is rejected. |
| 16 | Get nonexistent product | Verifies retrieving an unknown product is rejected. |
| 17 | Search products | Verifies products can be searched by name. |
| 18 | Case-insensitive search | Ensures searches work regardless of letter case. |
| 19 | Search with no match | Verifies an empty result is returned when no product matches. |
| 20 | Calculate inventory value | Verifies total inventory value is calculated correctly. |
| 21 | Empty inventory value | Ensures an empty inventory has a value of zero. |
| 22 | Low-stock products | Verifies products at or below the threshold are identified. |
| 23 | No low-stock products | Verifies an empty result when no products are below the threshold. |
| 24 | Negative low-stock threshold | Ensures negative thresholds are rejected. |
| 25 | Non-numeric price | Ensures invalid price types are rejected. |
| 26 | Non-integer quantity | Ensures invalid quantity types are rejected. |
| 27 | Non-integer stock update | Ensures invalid stock update types are rejected. |
| 28 | Non-integer low-stock threshold | Ensures invalid threshold types are rejected. |

### Integration Test Cases

| # | Test Case | Purpose |
|---:|---|---|
| 29 | Save and load inventory | Verifies inventory can be persisted and restored correctly. |
| 30 | Saved inventory is valid JSON | Verifies the generated file contains valid JSON data. |
| 31 | Missing JSON file | Ensures loading a nonexistent file raises the expected error. |
| 32 | Malformed JSON | Ensures invalid JSON content is rejected. |
| 33 | Invalid JSON structure | Ensures JSON with an unexpected structure is rejected. |
| 34 | Invalid product data | Ensures invalid product information loaded from JSON is rejected. |

### Why These Test Cases Were Chosen

The test suite was designed to cover both the normal behavior of the inventory module
and situations that could cause incorrect or unreliable results.

Normal-operation tests verify that the core functionality works correctly. Validation
tests verify that invalid user or product data cannot enter the system. Edge-case tests,
such as zero stock and empty search results, verify boundary behavior. Integration tests
verify that the JSON persistence layer works correctly with the inventory management
logic.

Together, these tests provide coverage of the module's main functionality, error
conditions, and persistence behavior while supporting the project's Test-Driven
Development approach.

## 🔄 Test-Driven Development (TDD)

This project follows the basic **Test-Driven Development** cycle:

```text
Write Tests
     ↓
Run Tests
     ↓
Tests Fail - RED
     ↓
Implement Functionality
     ↓
Run Tests Again
     ↓
Tests Pass - GREEN
     ↓
Refactor Code
     ↓
Run Tests Again
     ↓
Repeat
```

### 🔴 TDD RED Stage

The tests were created before the `InventoryManager` implementation.

Running the tests before implementation produced import failures because the required `InventoryManager` class had not yet been implemented.

This demonstrated the initial **RED** stage of the TDD process.

### 🟢 TDD GREEN Stage

After implementing the required functionality, the complete test suite passed successfully.

Current result:

```text
34 passed
100% coverage
```

### 🔵 Refactoring Stage

After achieving a passing test suite, the implementation was refactored to improve:

- Type hints
- Input validation
- Code organization
- Documentation
- Error handling
- Readability
- Maintainability

The refactoring was performed while keeping the existing automated tests passing.

---

## 🔄 Development Workflow

The overall development workflow used for this project is:

```text
Clone Repository
       ↓
Create Virtual Environment
       ↓
Install Dependencies
       ↓
Write Tests
       ↓
Run Tests
       ↓
Implement / Modify Code
       ↓
Run Tests Again
       ↓
Check Code Coverage
       ↓
Refactor Code
       ↓
Run Tests Again
       ↓
Commit Changes
       ↓
Push to GitHub
```

---

## 🏗️ Project Structure

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
```

### Directory Description

| File / Directory | Purpose |
|---|---|
| `inventory/` | Main application package |
| `inventory/manager.py` | Contains the `InventoryManager` implementation |
| `inventory/__init__.py` | Initializes the Python package |
| `tests/` | Automated test suite |
| `tests/test_inventory.py` | Unit tests |
| `tests/test_inventory_integration.py` | Integration tests |
| `pytest.ini` | Pytest configuration |
| `requirements.txt` | Project dependencies |
| `.gitignore` | Files excluded from version control |
| `README.md` | Project documentation |

---

## 💻 Example Usage

The `InventoryManager` class provides several operations for managing inventory.

### Create an Inventory

```python
from inventory.manager import InventoryManager

inventory = InventoryManager()
```

### Add a Product

```python
inventory.add_product(
    "P001",
    "Keyboard",
    1200.00,
    10,
)
```

### Get a Product

```python
product = inventory.get_product("P001")

print(product)
```

### List Products

```python
products = inventory.list_products()

print(products)
```

### Update Stock

```python
inventory.update_stock("P001", 15)
```

### Search Products

```python
results = inventory.search_products("keyboard")

print(results)
```

### Calculate Inventory Value

```python
value = inventory.calculate_inventory_value()

print(value)
```

### Find Low-Stock Products

```python
low_stock = inventory.get_low_stock_products(
    threshold=5
)

print(low_stock)
```

---

## 💾 JSON Persistence

The inventory manager supports saving and loading inventory data using JSON files.

### Save Inventory

```python
inventory.save_to_json("inventory.json")
```

Example generated JSON:

```json
[
    {
        "id": "P001",
        "name": "Keyboard",
        "price": 1200.0,
        "quantity": 10
    },
    {
        "id": "P002",
        "name": "Mouse",
        "price": 600.0,
        "quantity": 5
    }
]
```

### Load Inventory

```python
inventory.load_from_json("inventory.json")
```

The saved inventory can then be restored into an `InventoryManager` instance.

---

## 🛡️ Error Handling

The application uses Python exceptions to handle invalid operations.

The project uses exceptions including:

```text
ValueError
TypeError
KeyError
FileNotFoundError
json.JSONDecodeError
```

For example, attempting to add a product with a negative quantity is rejected:

```python
inventory.add_product(
    "P003",
    "Monitor",
    15000.00,
    -5,
)
```

The invalid quantity is validated and rejected instead of being added to the inventory.

---

## 🧹 Code Quality

The implementation was refactored after achieving a passing test suite.

The current implementation includes:

- Type hints
- Static validation helper methods
- Descriptive docstrings
- Clear method names
- Input validation
- Explicit exception handling
- Separation of application and test code
- JSON persistence handling
- Maintainable project structure

---

## 📋 Test Case Summary

| Test Category | Number of Tests |
|---|---:|
| Inventory initialization | 1 |
| Product addition | 3 |
| Product removal | 2 |
| Product retrieval | 2 |
| Stock management | 5 |
| Product searching | 3 |
| Inventory calculations | 2 |
| Low-stock detection | 3 |
| Input validation | 7 |
| JSON integration | 6 |
| **Total** | **34** |

---

## 📈 Current Project Status

### Completed

- [x] Project structure created
- [x] Inventory management module implemented
- [x] Unit tests implemented
- [x] Integration tests implemented
- [x] TDD workflow demonstrated
- [x] Input validation implemented
- [x] JSON persistence implemented
- [x] Code refactored for quality
- [x] 34 automated tests passing
- [x] 100% code coverage
- [x] Git version control configured
- [x] GitHub repository created
- [x] Project documentation created

### Planned Improvements

Possible future improvements include:

- Continuous Integration using GitHub Actions
- Additional test cases
- More detailed API documentation
- Logging support
- Database persistence
- Command-line interface
- User interface
- Performance testing

---

## 🎓 Internship Project

This project was developed as part of a **Python Programming Internship**.

The project demonstrates practical experience in:

- Python programming
- Object-oriented programming
- Automated testing
- Unit testing
- Integration testing
- Test-Driven Development
- Input validation
- Exception handling
- JSON data persistence
- Code refactoring
- Code coverage
- Git and GitHub

---