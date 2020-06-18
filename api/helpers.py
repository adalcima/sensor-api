from statistics import median, StatisticsError


def get_median(values):
    try:
        return median(values)
    except StatisticsError:
        return None


def get_quartiles():
    pass
