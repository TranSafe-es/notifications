from django.test import TestCase
from rest_framework.test import APIClient
import uuid


class DataTestCase(TestCase):
    def setUp(self):
        pass

    def test_objects(self):
        client = APIClient()
        """
        # send email
        url = "/api/v1/notification/email/"
        data = {'email': 'pgrm.arcf@gmail.com',
                'message': 'Ola!'}
        response = client.post(path=url, data=data)
        # print response.data, response.status_code
        self.assertEqual(response.status_code, 200)

        # send sms
        url = "/api/v1/notification/sms/"
        data = {'number': '+351914316075',
                'message': 'Ola!'}
        response = client.post(path=url, data=data)
        self.assertEqual(response.status_code, 200)
        # print response.data, response.status_code
        """
        # send messenger
        url = "/api/v1/notification/messenger/"
        data = {'profile_id': '140064409787860',
                'message': 'Ola!'}
        response = client.post(path=url, data=data)
        self.assertEqual(response.status_code, 200)
        # print response.data
        # print response.data, response.status_code
