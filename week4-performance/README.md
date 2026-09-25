# Week 4 — Python Performance Optimization

## 1. Objective

The objective of this task was to identify and optimize a performance bottleneck in the Python Inventory Management application while preserving its existing functionality and correctness.

The optimization focused on the `calculate_inventory_value()` method in:

```text
inventory/manager.py
```

The task involved:

- Establishing a performance baseline.
- Profiling the application using Python's `cProfile`.
- Identifying the primary performance bottleneck.
- Optimizing the bottleneck.
- Verifying that the optimization did not break existing functionality.
- Measuring the optimized implementation using the same workload.
- Comparing the before-and-after performance results.
- Preserving the original and optimized implementations for review.

---

## 2. Application Overview

The project is a Python-based Inventory Management application.

The application provides functionality for:

- Adding products.
- Removing products.
- Retrieving individual products.
- Listing products.
- Updating stock quantities.
- Searching products by name.
- Calculating total inventory value.
- Identifying low-stock products.
- Saving inventory data to JSON.
- Loading inventory data from JSON.
- Validating product IDs, names, prices, and quantities.

The Week 4 optimization specifically targets the repeated calculation of total inventory value.

---

## 3. Original Implementation

The original `calculate_inventory_value()` implementation calculated the total inventory value by iterating through every product each time the method was called.

The original implementation was:

```python
def calculate_inventory_value(self) -> float:
    """Calculate the total monetary value of all inventory."""
    return sum(
        product["price"] * product["quantity"]
        for product in self._products.values()
    )
```

For every call, the method traversed the complete product collection and calculated:

```text
price × quantity
```

for every product.

For an inventory containing 10,000 products, one calculation required processing all 10,000 products.

The benchmark executed the calculation 1,000 times, resulting in approximately:

```text
10,000 products × 1,000 calculations
= 10,000,000 product-level calculations
```

This repeated traversal was identified as the main performance bottleneck.

The original implementation is preserved in:

```text
week4-performance/original/manager.py
```

---

## 4. Baseline Performance Measurement

Before modifying the application, a performance baseline was established.

### Benchmark Workload

| Metric | Value |
|---|---:|
| Number of products | 10,000 |
| Number of calculations | 1,000 |
| Inventory value | 535,780,000.00 |

### Baseline Result

```text
Total execution time: 1.440711 seconds
Average calculation time: 0.001440711 seconds
```

The complete baseline result is stored in:

```text
week4-performance/benchmarks/baseline.txt
```

---

## 5. Performance Profiling

Python's `cProfile` was used to investigate where the application was spending most of its execution time.

The baseline profiling results identified `calculate_inventory_value()` as the primary bottleneck.

Important baseline profiling observations included:

```text
manager.py:186(calculate_inventory_value)
builtins.sum
manager.py:188(<genexpr>)
```

The profiler showed that repeated calls to `calculate_inventory_value()` spent significant time in:

- Python's built-in `sum()` function.
- The generator expression.
- Repeated traversal of all products.
- Repeated multiplication of product price and quantity.

The baseline profile contained approximately:

```text
10,268,264 function calls
```

and the inventory-value calculation was responsible for the majority of the measured execution time.

The complete baseline profiling output is stored in:

```text
week4-performance/benchmarks/baseline_profile.txt
```

---

## 6. Identified Bottleneck

The primary bottleneck was the repeated recalculation of the complete inventory value.

The original algorithm was effectively:

```text
For every calculation:
    For every product:
        Calculate price × quantity
    Add all product values together
```

Therefore, the time complexity of `calculate_inventory_value()` was:

```text
O(n)
```

where `n` represents the number of products in the inventory.

When the method was called repeatedly, the same inventory data was traversed again and again even though the inventory itself had not changed.

This made the calculation inefficient for larger inventories and repeated queries.

---

## 7. Optimization Approach

The optimization introduced an incrementally maintained cached inventory value.

A new internal attribute was added:

```python
self._total_inventory_value: float = 0.0
```

Instead of recalculating the entire inventory value every time, the application now updates this cached value whenever the inventory changes.

### Adding a Product

When a product is added, its value is immediately added to the cached total:

```python
self._total_inventory_value += float(price) * quantity
```

### Removing a Product

When a product is removed, its value is subtracted from the cached total:

```python
self._total_inventory_value -= (
    product["price"] * product["quantity"]
)
```

### Updating Stock

When stock quantity changes, only the difference is applied:

```python
self._total_inventory_value += (
    product["price"] * (quantity - old_quantity)
)
```

### Loading from JSON

When inventory data is loaded from JSON, the cached value is reset:

```python
self._products = {}
self._total_inventory_value = 0.0
```

The existing `add_product()` method is then used to rebuild the inventory and update the cached total while preserving the existing validation logic.

---

## 8. Optimized Implementation

The optimized `calculate_inventory_value()` method is now:

```python
def calculate_inventory_value(self) -> float:
    """Return the total monetary value of all inventory."""
    return self._total_inventory_value
```

The method no longer iterates over every product.

The time complexity has therefore changed from:

```text
O(n)
```

to:

```text
O(1)
```

The optimized implementation is preserved in:

```text
week4-performance/optimized/manager.py
```

---

## 9. Complexity Comparison

### Original Implementation

```text
calculate_inventory_value()
        |
        v
Iterate through all products
        |
        v
price × quantity for each product
        |
        v
sum all values
```

Time complexity:

```text
O(n)
```

where `n` is the number of products.

### Optimized Implementation

```text
calculate_inventory_value()
        |
        v
Return cached total
```

Time complexity:

```text
O(1)
```

The cached value is maintained during inventory mutations instead of being recalculated during every query.

---

## 10. Performance Results

The exact same workload was used for the baseline and optimized benchmark.

### Workload

| Metric | Value |
|---|---:|
| Products | 10,000 |
| Iterations | 1,000 |
| Inventory value | 535,780,000.00 |

### Before vs After

| Metric | Baseline | Optimized |
|---|---:|---:|
| Execution time | 1.440711 s | 0.031646 s |
| Average calculation time | 0.001440711 s | 0.000031646 s |
| Complexity | O(n) | O(1) |

### Performance Improvement

Time saved:

```text
1.440711 - 0.031646
= 1.409065 seconds
```

Execution-time reduction:

```text
97.80%
```

Measured speedup:

```text
45.53×
```

Therefore, under the benchmark workload, the optimized implementation completed the benchmark approximately **45.53 times faster** than the original implementation.

The complete comparison is stored in:

```text
week4-performance/benchmarks/comparison.txt
```

---

## 11. Optimized Profiling

After implementing the optimization, the application was profiled again using:

```powershell
python -m cProfile -s cumulative -m benchmarks.benchmark
```

The optimized profile showed that `calculate_inventory_value()` no longer performed the previous full traversal.

The optimized profile contains the method:

```text
manager.py:202(calculate_inventory_value)
```

with negligible cumulative execution time.

The previous:

```text
builtins.sum
```

bottleneck associated with the inventory-value calculation was no longer present.

The optimized profiling output is stored in:

```text
week4-performance/benchmarks/optimized_profile.txt
```

The optimized profile also shows that the remaining measurable work is primarily associated with creating and populating the 10,000-product inventory, particularly:

```text
create_inventory()
add_product()
```

This confirms that the original repeated inventory-value calculation was successfully removed as the dominant bottleneck.

---

## 12. Correctness Validation

Performance improvements are only useful if application behavior remains correct.

The optimized implementation was therefore validated through the existing automated test suite and additional direct checks.

### Add Product

Two products were added:

```text
Laptop: 1000 × 10 = 10000
Mouse:    50 × 20 =  1000
```

Expected total:

```text
11000.0
```

Result:

```text
After add: 11000.0
```

### Update Stock

The laptop quantity was changed from 10 to 15.

The updated total was:

```text
16000.0
```

Result:

```text
After stock update: 16000.0
```

### Remove Product

The mouse product was removed.

The remaining inventory value was:

```text
15000.0
```

Result:

```text
After remove: 15000.0
```

### Load From JSON

An inventory containing the same laptop and mouse products was loaded from a JSON file.

The resulting inventory value was:

```text
11000.0
```

Result:

```text
After JSON load: 11000.0
```

These checks confirmed that the cached total remains synchronized when products are added, stock is changed, products are removed, and inventory is loaded from JSON.

---

## 13. Automated Test Results

The existing automated test suite was executed after the optimization.

Command:

```powershell
pytest
```

Result:

```text
34 passed
```

No existing tests failed after the optimization.

---

## 14. Code Coverage

Code coverage was measured using:

```powershell
pytest --cov=inventory --cov-report=term-missing
```

### Final Coverage

| File | Coverage |
|---|---:|
| `inventory/__init__.py` | 100% |
| `inventory/manager.py` | 100% |
| **Total** | **100%** |

The optimized `manager.py` contains 80 statements and all 80 statements were covered.

Final result:

```text
34 passed
80 statements
0 missed
100% coverage
```

This confirms that the optimization was implemented without reducing the existing test coverage.

---

## 15. Benchmark Methodology

The benchmark is implemented in:

```text
benchmarks/benchmark.py
```

The benchmark creates an inventory containing:

```text
10,000 products
```

Each product is assigned:

- A unique product ID.
- A product name.
- A price.
- A quantity.

The benchmark then performs:

```text
1,000 inventory-value calculations
```

using:

```python
inventory.calculate_inventory_value()
```

The benchmark uses Python's `timeit` module to measure execution time.

The same workload was used for both the baseline and optimized implementations.

This ensures that the performance comparison is based on the same number of products and calculation iterations.

---

## 16. Reproducing the Tests

Activate the project's virtual environment and run:

```powershell
pytest
```

Run coverage:

```powershell
pytest --cov=inventory --cov-report=term-missing
```

Run the performance benchmark:

```powershell
python -m benchmarks.benchmark
```

Run the profiler:

```powershell
python -m cProfile -s cumulative -m benchmarks.benchmark
```

The benchmark uses:

```text
Products: 10,000
Iterations: 1,000
```

---

## 17. Project Files

The Week 4 performance work is organized as follows:

```text
week4-performance/
├── benchmarks/
│   ├── baseline.txt
│   ├── baseline_profile.txt
│   ├── comparison.txt
│   ├── optimized.txt
│   └── optimized_profile.txt
│
├── optimized/
│   └── manager.py
│
├── original/
│   └── manager.py
│
└── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `baseline.txt` | Original implementation benchmark result |
| `baseline_profile.txt` | Original `cProfile` output |
| `optimized.txt` | Optimized implementation benchmark result |
| `optimized_profile.txt` | Optimized `cProfile` output |
| `comparison.txt` | Before-and-after performance comparison |
| `original/manager.py` | Original implementation |
| `optimized/manager.py` | Optimized implementation |
| `README.md` | Week 4 documentation |

---

## 18. Before and After Summary

### Before Optimization

```text
calculate_inventory_value()
        ↓
Iterate over every product
        ↓
Calculate price × quantity
        ↓
Sum all values
```

Complexity:

```text
O(n)
```

Benchmark:

```text
1.440711 seconds
```

### After Optimization

```text
Inventory mutations
        ↓
Update cached total
        ↓
calculate_inventory_value()
        ↓
Return cached total
```

Complexity:

```text
O(1)
```

Benchmark:

```text
0.031646 seconds
```

### Final Measured Improvement

```text
Execution-time reduction: 97.80%
Speedup: 45.53×
```

---

## 19. Optimization Benefits

The optimization provides the following benefits:

- `calculate_inventory_value()` no longer scans the complete inventory for every call.
- Repeated inventory-value queries now execute in constant time.
- The cached total is updated only when inventory data changes.
- Existing validation behavior is preserved.
- JSON loading continues to use the existing product validation path.
- Existing automated tests continue to pass.
- Code coverage remains at 100%.
- The profiler confirms that the original calculation bottleneck has been removed.
- The original and optimized implementations are preserved separately for comparison.
- The benchmark demonstrates a substantial reduction in execution time for the tested workload.

---

## 20. Conclusion

Performance profiling identified the repeated calculation of total inventory value as the primary bottleneck in the Inventory Management application.

The original implementation recalculated the complete inventory value every time `calculate_inventory_value()` was called. With 10,000 products and 1,000 calculations, this resulted in approximately 10 million product-level calculations.

The optimization introduced an incrementally maintained `_total_inventory_value` cache. The cache is updated when products are added, removed, or when their stock quantity changes. JSON loading resets and rebuilds the cached total through the existing `add_product()` validation path.

As a result, `calculate_inventory_value()` changed from an **O(n)** operation to an **O(1)** operation.

Using the same benchmark workload, execution time decreased from:

```text
1.440711 seconds
```

to:

```text
0.031646 seconds
```

This represents:

```text
97.80% execution-time reduction
45.53× speedup
```

The optimized implementation also passed all:

```text
34 automated tests
```

with:

```text
100% code coverage
```

The profiling results further confirmed that the previous `sum()` and generator-expression bottleneck was eliminated.

The Week 4 task therefore demonstrates a complete performance-optimization workflow:

```text
Baseline Measurement
        ↓
Performance Profiling
        ↓
Bottleneck Identification
        ↓
Algorithm Optimization
        ↓
Correctness Validation
        ↓
Performance Re-measurement
        ↓
Before/After Comparison
        ↓
Documentation
```

---

## 21. Final Performance Summary

| Category | Result |
|---|---:|
| Products tested | 10,000 |
| Calculations tested | 1,000 |
| Baseline execution time | 1.440711 s |
| Optimized execution time | 0.031646 s |
| Time saved | 1.409065 s |
| Execution-time reduction | 97.80% |
| Speedup | 45.53× |
| Original complexity | O(n) |
| Optimized complexity | O(1) |
| Automated tests | 34 passed |
| Code coverage | 100% |
| Functionality preserved | Yes |

---

**Week 4 Status: Performance optimization completed and validated.**
