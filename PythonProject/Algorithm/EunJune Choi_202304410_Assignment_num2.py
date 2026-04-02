def find_duplicate(numbers):
    seen_values = set()
    for num in numbers:
        if num in seen_values:
            return num
        seen_values.add(num)
    return "No duplicates found"

list_with_duplicates = [3, 1, 5, 8, 4, 5, 9]
print(f" List: {list_with_duplicates}")
print(f"find duplicate: {find_duplicate(list_with_duplicates)}")

list_no_duplicates = [10, 20, 30, 40, 50]
print(f"\nlist: {list_no_duplicates}")
print(f"find_duplicate: {find_duplicate(list_no_duplicates)}")