Group: Lauren Sdun, Julia Baumgarten



# Bubble sort method
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Merge sort method
def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    
L = [0] * n1
R = [0] * n2

for i in range(n1):
    L[i] = arr[left + i]
for j in range(n2):
    R[j] = arr[mid + 1 + j]

i = 0
j = 0
k = left

while i < n1 and j < n2:
    if L[i] <= R[j]:
        arr[k] = L[i]
        i += 1
    else:
        arr[k] = R[j]
        j += 1
    k +=1
    
while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
