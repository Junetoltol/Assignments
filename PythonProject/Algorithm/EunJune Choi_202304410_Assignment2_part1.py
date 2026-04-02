def maximum_subarray(A):
    current_max = A[0]
    global_max = A[0]
    for i in range(1, len(A)):
        current_max = max(A[i], current_max + A[i])
        if current_max > global_max:
            global_max = current_max
    return global_max
A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Maximum Subarray Sum:", maximum_subarray(A))
