import json
import time
import unittest

import pytest
from api import create_app, db
from api.models import Reading


class SensorRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.device_uuid = 'test_device'

        # Setup the SQLite DB
        db.drop_all()
        db.create_all()

        # Setup some sensor data
        reading_1 = Reading(
            device_uuid=self.device_uuid,
            type='temperature',
            value=22,
            date_created=int(time.time()) - 100,
        )
        db.session.add(reading_1)

        reading_2 = Reading(
            device_uuid=self.device_uuid,
            type='temperature',
            value=50,
            date_created=int(time.time()) - 50,
        )
        db.session.add(reading_2)

        reading_3 = Reading(
            device_uuid=self.device_uuid,
            type='temperature',
            value=100,
            date_created=int(time.time()),
        )
        db.session.add(reading_3)

        reading_4 = Reading(
            device_uuid=self.device_uuid,
            type='temperature',
            value=22,
            date_created=int(time.time()),
        )
        db.session.add(reading_4)

        db.session.commit()

    def test_device_readings_get(self):
        # Given a device UUID
        # When we make a request with the given UUID
        request = self.client.get(f'/devices/{self.device_uuid}/readings')

        # Then we should receive a 200
        self.assertEqual(request.status_code, 200)

        # And the response data should have four sensor readings
        self.assertTrue(len(json.loads(request.data)) == 4)

    def test_device_readings_post(self):
        # Given a device UUID
        # When we make a request with the given UUID to create a reading
        request = self.client.post(
            f'/devices/{self.device_uuid}/readings',
            data=json.dumps({'type': 'temperature', 'value': 100}),
        )

        # Then we should receive a 201
        self.assertEqual(request.status_code, 201)

        # And when there is a missing field
        request = self.client.post(
            f'/devices/{self.device_uuid}/readings',
            data=json.dumps({'type': 'temperature'}),
        )

        # Then we should receive a 400
        self.assertEqual(request.status_code, 400)

        # And when we send invalid value for temperature or humidity
        request = self.client.post(
            f'/devices/{self.device_uuid}/readings',
            data=json.dumps({'type': 'temperature', 'value': 101}),
        )

        # Then we should receive a 400
        self.assertEqual(request.status_code, 400)

        # And when we check for readings in the db
        rows = Reading.query.filter_by(device_uuid=self.device_uuid).count()

        # We should have five
        self.assertTrue(rows == 5)

    def test_device_readings_get_temperature(self):
        # Given a device UUID
        # When we filter by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings?type=temperature'
        )

        # Then the response data should have four sensor readings
        self.assertTrue(len(json.loads(request.data)) == 4)

    def test_device_readings_get_humidity(self):
        # Given a device UUID
        # When we filter by humidity type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings?type=humidity'
        )

        # Then the response data should have 0 sensor readings
        self.assertTrue(len(json.loads(request.data)) == 0)

    def test_device_readings_get_past_dates(self):
        # Given a device UUID
        # When we filter by end date using now
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings?end={int(time.time())}'
        )

        # Then the response data should have four sensor readings
        self.assertTrue(len(json.loads(request.data)) == 4)

    def test_device_readings_min(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's min sensor reading.
        """
        # self.assertTrue(False)
        pass

    def test_device_readings_max(self):
        # Given a device UUID
        # When we make a request to get max value by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings/max?type=temperature'
        )

        # Then the response data value should be 100
        self.assertEqual(json.loads(request.data)[0]['value'], 100)

    def test_device_readings_median(self):
        # Given a device UUID
        # When we make a request to get median value by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings/median?type=temperature'
        )

        # Then the response data should have 0 sensor readings
        self.assertTrue(len(json.loads(request.data)) == 0)

        # Given UUID to create new reading
        request = self.client.post(
            f'/devices/{self.device_uuid}/readings',
            data=json.dumps({'type': 'temperature', 'value': 100}),
        )

        # When we make a request to get median value by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings/median?type=temperature'
        )

        # Then the response data should have one sensor readings
        self.assertTrue(len(json.loads(request.data)) == 1)

    def test_device_readings_mean(self):
        # Given a device UUID
        # When we make a request to get mean value by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings/mean?type=temperature'
        )

        # Then the response data value should be 100
        self.assertEqual(json.loads(request.data)['value'], 48.5)

    def test_device_readings_mode(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's mode sensor reading value.
        """
        # self.assertTrue(False)
        pass

    def test_device_readings_quartiles(self):
        # Given a device UUID, start and end range
        start = int(time.time()) - 50000
        end = int(time.time())

        # When we make a request to get quartiles by temperature type
        request = self.client.get(
            f'/devices/{self.device_uuid}/readings/quartiles?type=temperature&start={start}&end={end}'
        )

        # Then the quartile_1 should be 22 and quartile_3 should be 75
        self.assertEqual(json.loads(request.data)['quartile_1'], 22)
        self.assertEqual(json.loads(request.data)['quartile_3'], 75)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
