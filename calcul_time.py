import time


def operation():
    return 69 + 420


def mesure(n):
    start_time = time.time()
    for i in range(n):
        operation()
    end_time = time.time()
    duration = end_time - start_time
    return duration / n


print(f"{mesure(100000):.10f} secondes/operation")
