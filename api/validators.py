def validate_sensor_value(sensor_type, value):
    restricted_types = ['temperature', 'humidity']
    if sensor_type in restricted_types:
        return True if value in range(0, 101) else False

    return True
