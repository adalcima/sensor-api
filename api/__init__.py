import json
import time

from api.config import app_config
from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name=None):
    from api.models import Reading

    if config_name is None:
        config_name = 'development'

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route(
        '/devices/<string:device_uuid>/readings', methods=['POST', 'GET']
    )
    def request_device_readings(device_uuid):
        """
        This endpoint allows clients to POST or GET data specific sensor types.

        POST Parameters:
        * type -> The type of sensor (temperature or humidity)
        * value -> The integer value of the sensor reading
        * date_created -> The epoch date of the sensor reading.
            If none provided, we set to now.

        Optional Query Parameters:
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        * type -> The type of sensor value a client is looking for
        """

        if request.method == 'POST':
            # Grab the post parameters
            post_data = json.loads(request.data)
            sensor_type = post_data.get('type')
            value = post_data.get('value')
            date_created = post_data.get('date_created', int(time.time()))

            # Insert data into db
            reading = Reading(
                device_uuid=device_uuid,
                type=sensor_type,
                value=value,
                date_created=date_created,
            )
            db.session.add(reading)
            db.session.commit()

            # Return success
            return 'success', 201
        else:
            # Execute the query
            readings = Reading.query.all()
            results = []

            for reading in readings:
                obj = {
                    'device_uuid': reading.device_uuid,
                    'type': reading.type,
                    'value': reading.value,
                    'date_created': reading.date_created,
                }
                results.append(obj)

            # Return the JSON
            return (
                jsonify(results),
                200,
            )

    @app.route('/devices/<string:device_uuid>/readings/max', methods=['GET'])
    def request_device_readings_max(device_uuid):
        """
        This endpoint allows clients to GET the max sensor reading for a device

        Mandatory Query Parameters:
        * type -> The type of sensor value a client is looking for

        Optional Query Parameters
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        """

        return 'Endpoint is not implemented', 501

    @app.route(
        '/devices/<string:device_uuid>/readings/median', methods=['GET']
    )
    def request_device_readings_median(device_uuid):
        """
        This endpoint allows clients to GET the median sensor reading for a
        device.

        Mandatory Query Parameters:
        * type -> The type of sensor value a client is looking for

        Optional Query Parameters
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        """

        return 'Endpoint is not implemented', 501

    @app.route('/devices/<string:device_uuid>/readings/mean', methods=['GET'])
    def request_device_readings_mean(device_uuid):
        """
        This endpoint allows clients to GET the mean sensor readings for a
        device.

        Mandatory Query Parameters:
        * type -> The type of sensor value a client is looking for

        Optional Query Parameters
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        """

        return 'Endpoint is not implemented', 501

    @app.route(
        '/devices/<string:device_uuid>/readings/quartiles', methods=['GET']
    )
    def request_device_readings_quartiles(device_uuid):
        """
        This endpoint allows clients to GET the 1st and 3rd quartile
        sensor reading value for a device.

        Mandatory Query Parameters:
        * type -> The type of sensor value a client is looking for
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        """

        return 'Endpoint is not implemented', 501

    @app.route('/devices/readings', methods=['GET'])
    def request_readings_summary():
        """
        This endpoint allows clients to GET a full summary
        of all sensor data in the database per device.

        Optional Query Parameters
        * type -> The type of sensor value a client is looking for
        * start -> The epoch start time for a sensor being created
        * end -> The epoch end time for a sensor being created
        """

        return 'Endpoint is not implemented', 501

    return app
