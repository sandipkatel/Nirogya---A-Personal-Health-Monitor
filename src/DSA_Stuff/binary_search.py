# Binary search
def binary_search(arr, target, low, high):
    if low > high:
        return False

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)

def search(arr, target):
    return binary_search(arr, target, 0, len(arr)-1)