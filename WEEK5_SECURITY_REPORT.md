# Week 5 Security Audit Report

## 1. Overview

This report documents the security audit and security improvements performed on the Python Inventory Management project as part of Week 5.

The audit focused on:

- Application-level input validation
- Inventory data integrity
- JSON inventory loading
- Numeric input handling
- Static security analysis
- Dependency vulnerability checking
- Security regression testing

The following tools were used during the audit:

- Bandit
- pip-audit
- Pytest
- Pytest Coverage

---

## 2. Security Audit Methodology

The inventory management application was reviewed for potential issues involving:

1. Invalid or unsafe input values.
2. Numeric validation weaknesses.
3. Inventory data integrity during file imports.
4. Handling of invalid JSON inventory data.
5. Python code security issues.
6. Known vulnerabilities in project dependencies.

The existing test suite was also extended with security-focused regression tests to verify that identified issues were fixed and remain fixed in future changes.

---

## 3. Security Finding 1 — Non-Atomic JSON Inventory Loading

### Severity

**Medium**

### Category

**Data Integrity / Improper Error Handling**

### Description

The original `load_from_json()` implementation cleared the current inventory before completely validating all products contained in the JSON file.

If a JSON file contained multiple products and a later product failed validation, the inventory could be left partially loaded or the previously existing inventory could be lost.

For example, an imported file could contain:

1. A valid product.
2. Another product containing an invalid quantity.

The original implementation could clear the existing inventory and then fail while processing the invalid product.

### Potential Exploitation / Impact

An invalid or malformed inventory file could cause unintended modification of the application's current inventory state.

If an attacker or untrusted process were able to provide or replace an inventory JSON file, a deliberately malformed file could cause the existing inventory data to be lost or partially replaced when the file was loaded.

This represents a data integrity risk.

### Reproduction

A security regression test was created containing:

- An existing valid inventory item.
- A JSON file containing a valid product.
- A second product with an invalid negative quantity.

The test attempted to load the invalid file and then verified that the original inventory item was still present.

### Original Vulnerable Behavior

The original implementation reset the inventory before all products had been successfully validated.

As a result, a failed import could modify the current inventory even though the import operation itself failed.

### Fix Implemented

`load_from_json()` was changed to validate the complete JSON dataset using a temporary `InventoryManager`.

The existing inventory is updated only after every product has been successfully validated and added to the temporary inventory.

The new behavior is effectively atomic:

- If all products are valid, the new inventory is committed.
- If any product is invalid, the operation fails and the existing inventory remains unchanged.

### Security Test Added

`test_failed_load_does_not_modify_existing_inventory`

This test verifies that a failed JSON import does not destroy or partially replace the existing inventory.

---

## 4. Security Finding 2 — Non-Finite Product Prices

### Severity

**Medium**

### Category

**Improper Input Validation**

### Description

The original product price validation checked whether the value was numeric and whether it was negative.

However, Python floating-point values such as:

```python
float("nan")
```

and:

```python
float("inf")
```

are numeric values but do not represent valid finite product prices.

The original validation therefore allowed non-finite values.

### Potential Exploitation / Impact

An invalid numeric value could be inserted into the inventory as a product price.

For example:

```python
float("nan")
```

could previously pass the numeric type validation.

This could introduce invalid values into inventory calculations and cause incorrect or unexpected application behavior.

Similarly, positive or negative infinity could be stored as a product price.

This represents an input validation and data integrity issue.

### Reproduction

Two security regression tests were added:

`test_nan_price_is_rejected`

and:

`test_infinite_price_is_rejected`

Before the fix, both tests failed because the invalid values were accepted.

### Fix Implemented

The price validation was strengthened using Python's `math.isfinite()` function.

The application now requires product prices to:

- Be numeric.
- Be finite.
- Not be negative.

The updated validation rejects values such as:

```python
float("nan")
float("inf")
float("-inf")
```

with a `ValueError`.

### Security Tests Added

`test_nan_price_is_rejected`

Verifies that `NaN` cannot be used as a product price.

`test_infinite_price_is_rejected`

Verifies that infinity cannot be used as a product price.

---

## 5. Security Tests Added

Three security-focused regression tests were added to the existing test suite.

### Test 1 — NaN Price

`test_nan_price_is_rejected`

Purpose:

Verify that a `NaN` value cannot be stored as a product price.

### Test 2 — Infinite Price

`test_infinite_price_is_rejected`

Purpose:

Verify that positive infinity cannot be stored as a product price.

### Test 3 — Failed JSON Load

`test_failed_load_does_not_modify_existing_inventory`

Purpose:

Verify that an invalid JSON import cannot modify or destroy the existing inventory.

These tests provide regression protection for the security and data-integrity issues identified during the audit.

---

## 6. Security Tool Results

### 6.1 Bandit

Bandit was used to perform static security analysis of the `inventory` package.

Command used:

```bash
bandit -r inventory -f txt
```

Final result:

```text
No issues identified
```

Final scan statistics:

| Result | Count |
|---|---:|
| Lines scanned | 222 |
| Low severity | 0 |
| Medium severity | 0 |
| High severity | 0 |

The clean Bandit result indicates that no Bandit-detectable security issues were found in the scanned application code.

Bandit static analysis does not replace manual security review or application-level testing.

---

### 6.2 pip-audit

`pip-audit` was used to check the project's Python dependencies for known published vulnerabilities.

Command used:

```bash
pip-audit
```

Final result:

```text
No known vulnerabilities found
```

This indicates that pip-audit did not identify known vulnerabilities in the project's installed dependencies at the time of the audit.

A clean dependency audit does not guarantee that a package has no undiscovered or newly published vulnerabilities.

---

## 7. Test and Coverage Validation

After implementing the security fixes, the complete test suite was executed.

Command used:

```bash
pytest -v
```

Result:

```text
37 passed
```

All tests passed successfully.

### Code Coverage

Coverage was checked using:

```bash
pytest --cov=inventory --cov-report=term-missing
```

Result:

```text
100% coverage
```

The final coverage result showed:

- `inventory/manager.py`: 84 statements
- Statements covered: 84
- Overall coverage: 100%

This confirms that the implemented security changes are covered by the automated test suite.

---

## 8. Additional Validation

Git whitespace and patch validation was performed using:

```bash
git diff --check
```

Result:

```text
No issues
```

This confirmed that the changes did not contain whitespace errors detected by Git.

---

## 9. Areas Not Applicable to the Current Project

The current inventory management application is a Python application and does not currently implement:

- A web server
- Database-backed SQL queries
- User authentication
- Password storage
- Session management
- Encryption functionality

Therefore, vulnerabilities such as:

- SQL injection
- Web authentication vulnerabilities
- Session security issues
- Password storage vulnerabilities
- Encryption implementation weaknesses

were not applicable to the current implementation.

These areas were not artificially introduced into the project simply for the purpose of the security audit.

The audit instead focused on security issues relevant to the application's existing functionality.

---

## 10. Security Improvements Summary

| Area | Identified Issue | Resolution |
|---|---|---|
| JSON loading | Failed imports could modify existing inventory | Implemented atomic validation and commit |
| Price validation | `NaN` and infinity were accepted | Added `math.isfinite()` validation |
| Regression testing | Security issues lacked dedicated tests | Added three security-focused tests |
| Static analysis | Application code required security analysis | Completed Bandit scan |
| Dependency security | Dependencies required vulnerability checking | Completed pip-audit scan |
| Validation | Security changes required regression validation | Full test suite and coverage executed |

---

## 11. Files Modified

The following project files were modified for the Week 5 security work:

### `inventory/manager.py`

Security improvements:

- Added `math` for finite-number validation.
- Rejected `NaN` and infinite product prices.
- Changed JSON loading to validate imported data before replacing the current inventory.

### `tests/test_inventory.py`

Added security tests for:

- `NaN` product prices.
- Infinite product prices.

### `tests/test_inventory_integration.py`

Added a security regression test verifying that a failed JSON import does not modify the existing inventory.

### `WEEK5_SECURITY_REPORT.md`

Added this security audit report documenting:

- Security findings.
- Potential impact.
- Reproduction scenarios.
- Fixes.
- Security tests.
- Static analysis results.
- Dependency audit results.
- Final validation.

---

## 12. Final Validation Results

The following validation checks were completed after implementing the security fixes:

| Validation | Result |
|---|---|
| Pytest | 37 passed |
| Code coverage | 100% |
| Bandit | No issues identified |
| pip-audit | No known vulnerabilities found |
| Git diff check | Clean |

---

## 13. Final Security Status

The Week 5 security audit identified two application-level issues related to input validation and inventory data integrity.

The identified issues were addressed by:

1. Rejecting non-finite product prices such as `NaN` and infinity.
2. Making JSON inventory loading atomic so that a failed import does not modify the existing inventory.
3. Adding automated regression tests for the identified issues.
4. Running static security analysis with Bandit.
5. Checking project dependencies with pip-audit.
6. Running the complete automated test suite with 100% coverage.

The final validation completed successfully with:

- **37 tests passed**
- **100% code coverage**
- **Bandit: No issues identified**
- **pip-audit: No known vulnerabilities found**
- **Git diff check: Clean**

These changes improve the application's input validation and protect inventory data integrity during failed JSON imports.
