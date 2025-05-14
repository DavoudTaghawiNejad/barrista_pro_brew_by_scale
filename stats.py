def calculate_std_dev(data):
    n = len(data)
    mean = sum(data) / n
    squared_differences = [(x - mean) ** 2 for x in data]
    variance = sum(squared_differences) / (n - 1)  # Using n-1 for sample standard deviation
    std_dev = variance ** 0.5
    return std_dev
