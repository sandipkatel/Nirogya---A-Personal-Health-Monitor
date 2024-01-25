# QuickSort.py
import pandas as pd

def partition(S, low, high, col_index):
    """Find a pivot point based on a specific column"""
    mid = (low + high) // 2
    pivot = S[mid][col_index]
    left, right = low, high
    while left <= right:
        while S[left][col_index] < pivot:
            left += 1
        while S[right][col_index] > pivot:
            right -= 1
        if left <= right:
            S[left], S[right] = S[right], S[left]
            left += 1
            right -= 1
    return left

def quick_sort(S, low, high, col_index):
    """Sort a set of data by a given pivot point based on a specific column"""
    if low < high:
        pivotpoint = partition(S, low, high, col_index)
        quick_sort(S, low, pivotpoint - 1, col_index)
        quick_sort(S, pivotpoint, high, col_index)

def sort_csv_file(filename):
    df = pd.read_csv(filename)
    data_to_sort = df.values.tolist()
    # Apply quick_sort to each column separately
    for col_index in range(df.shape[1]):
        quick_sort(data_to_sort, 0, len(data_to_sort) - 1, col_index)

    sorted_df = pd.DataFrame(data_to_sort, columns=df.columns)
    sorted_df.to_csv("output0.csv", index=False)
    return sorted_df.columns

if __name__ == "__main__":
    columns = sort_csv_file("input.csv")
    print(f"CSV file sorted based on columns: {columns}")
