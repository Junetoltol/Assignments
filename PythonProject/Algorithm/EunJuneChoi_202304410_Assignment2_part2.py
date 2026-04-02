def kadane(arr):
    current_max = arr[0]
    global_max = arr[0]
    start = temp_start = 0
    end = 0

    for i in range(1, len(arr)):
        if arr[i] > current_max + arr[i]:
            current_max = arr[i]
            temp_start = i
        else:
            current_max += arr[i]

        if current_max > global_max:
            global_max = current_max
            start = temp_start
            end = i

    return global_max, start, end


def maximum_sum_submatrix(matrix):
    n = len(matrix)
    m = len(matrix[0])

    max_sum = float('-inf')
    best_left = best_right = best_top = best_bottom = 0

    for left in range(m):
        temp = [0] * n

        for right in range(left, m):
            for row in range(n):
                temp[row] += matrix[row][right]

            current_sum, top, bottom = kadane(temp)

            if current_sum > max_sum:
                max_sum = current_sum
                best_left = left
                best_right = right
                best_top = top
                best_bottom = bottom

    return max_sum, best_left, best_right, best_top, best_bottom


matrix = [
    [1, -2, 3, 4],
    [-1, 4, -5, -1],
    [2, -1, 2, 1]
]

print(maximum_sum_submatrix(matrix))
