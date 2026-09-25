import timeit

from inventory.manager import InventoryManager


NUM_PRODUCTS = 10_000
NUM_ITERATIONS = 1_000


def create_inventory() -> InventoryManager:
    inventory = InventoryManager()

    for i in range(NUM_PRODUCTS):
        inventory.add_product(
            product_id=f"P{i:05d}",
            name=f"Product {i}",
            price=100.0 + i,
            quantity=(i % 20) + 1,
        )

    return inventory


def benchmark_calculate_inventory_value() -> float:
    inventory = create_inventory()

    total = 0.0

    for _ in range(NUM_ITERATIONS):
        total = inventory.calculate_inventory_value()

    return total


def main() -> None:
    inventory = create_inventory()

    expected_value = inventory.calculate_inventory_value()

    elapsed = timeit.timeit(
        benchmark_calculate_inventory_value,
        number=1,
    )

    print("=== Week 4 Performance Benchmark ===")
    print(f"Products: {NUM_PRODUCTS:,}")
    print(f"Inventory value: {expected_value:,.2f}")
    print(f"Iterations: {NUM_ITERATIONS:,}")
    print(f"Total execution time: {elapsed:.6f} seconds")
    print(
        f"Average calculation time: "
        f"{elapsed / NUM_ITERATIONS:.9f} seconds"
    )


if __name__ == "__main__":
    main()