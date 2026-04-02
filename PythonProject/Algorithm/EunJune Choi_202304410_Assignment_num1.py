def find_max_appointments(appointments):
    if not appointments:
        return 0
    appointments.sort(key=lambda x: x[1])
    max_count = 1
    last_end_time = appointments[0][1]
    for i in range(1, len(appointments)):
        current_start_time = appointments[i][0]
        if current_start_time >= last_end_time:
            max_count += 1
            last_end_time = appointments[i][1]
    return max_count
patient_requests = [
    [9, 11],
    [9, 10],
    [10, 12],
    [11, 13],
    [12, 14]
]
max_scheduled = find_max_appointments(patient_requests)
print(f"reservation_request: {patient_requests}")
print(f"Max patient without overlap: {max_scheduled}")