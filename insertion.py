A = [9, 7, 1, 3]

for i in range(1, len(A)):
    key = A[i]
    j = i - 1
    while j >= 0 and A[j] > key:
        A[j+1] = A[j]
        j -= 1
    A[j+1] = key

print(A)