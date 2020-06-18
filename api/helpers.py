from statistics import median, StatisticsError


def get_median(values):
    try:
        return median(values)
    except StatisticsError:
        return None


def get_quartiles(values):
    sorted_values = sorted(values)
    mid = len(sorted_values) // 2

    if len(sorted_values) % 2 == 0:
        quartile_1 = get_median(sorted_values[:mid])
        quartile_3 = get_median(sorted_values[mid:])

    else:
        quartile_1 = get_median(sorted_values[:mid])
        quartile_3 = get_median(sorted_values[mid + 1 :])

    return (int(quartile_1), int(quartile_3))
