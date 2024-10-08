def bubble_sort(arr):
    n = len(arr)

    # Traverse through all elements in the list
    for i in range(n):
        # Last i elements are already sorted, so we don't need to check them
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Example usage:
my_list = [64, 34, 25, 12, 22, 11, 90]
print("Original List:", my_list)

# Applying Bubble Sort
bubble_sort(my_list)

print("Sorted List:", my_list)
