# -*- coding: utf-8 -*-

import json
import unittest

from packFlask.api import app
from packFlask import api


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Creates a testomg secret key for session management.
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['TESTING'] = True
        # app.config['SESSION_COOKIE_DOMAIN'] = None
        self.app = app.test_client()

    ###################################################
    ########   GET Tests
    ###################################################

    def test_good_api(self):
        """ Test if application wams about api level"""
        response = self.app.get('/api/0.9')
        assert "You have entered an invalid api version" in response.data

    def test_index_redirect(self):
        """ Test index redirect"""
        response = self.app.get('/', follow_redirects=True)
        assert "<h1>Welcome to City4Age Rest A" in response.data

    def test_api_redirect(self):
        """ Test Api redirect"""
        response = self.app.get('/api', follow_redirects=True)
        assert "<h1>Welcome to City4Age Rest A" in response.data

    ###################################################
    ########   POST Tests
    ###################################################

    def test_no_header(self):
        """ Test status code 400: when there isn't any content_type header"""
        response = self.app.post('/api/0.1/login',
                                 data="Not a json data format, and not header type json",
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        """ Test status code 400: when header is correct but data is not correct"""
        response = self.app.post('/api/0.1/login',
                                 data="Not a json data format, but we have good content type header",
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_invalid_login(self):
        """ Test if the user send invalid JSON fields for login into the system """
        response = self.app.post('/api/0.1/login',
                                 data=json.dumps(dict(username='admin', password11='admin')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 500)

    def test_wrong_login(self):
        """ Test if the system return error 401 unauthorized"""
        response = self.app.post('/api/0.1/login',
                                 data=json.dumps(dict(username='admin', password='admin12')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_ok_login(self):
        """ Test if the system returns 200 code login ok"""
        response = self.app.post('/api/0.1/login',
                                 data=json.dumps(dict(username='admin', password='admin')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_basic_search(self):
        """ Test if we got any results """
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'admin'  # This simulates and encrypted cookie with username "admin"
                sess['id'] = 6              # and user id = 6
        response = c.post('/api/0.1/search',
                          data=json.dumps(dict(table='user_in_system',
                                               criteria={'username': 'admin'},
                                               limit=100,
                                               order_by='desc'
                                               )),
                          content_type='application/json',
                          follow_redirects=True)

        assert "No data found with this filters" not in response.data and response.status_code == 200

    def test_search_limit(self):
        """ Test if a search has a limit"""
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['id'] = 6
        response = c.post('/api/0.1/search',
                          data=json.dumps(dict(table='user_in_system',
                                               criteria={'username': 'admin'},
                                               limit=1,
                                               order_by='desc'
                                               )),
                          content_type='application/json',
                          follow_redirects=True)

        # todo we need to add more data
        assert response.data.count('admin') == 1 and response.status_code == 200

    def test_search_offset(self):
        """ Test if a search has a offset"""
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['id'] = 6
        response = c.post('/api/0.1/search',
                          data=json.dumps(dict(table='user_in_system',
                                               criteria={'username': 'admin'},
                                               limit=100,
                                               order_by='desc',
                                               offset=1,
                                               )),
                          content_type='application/json',
                          follow_redirects=True)

        assert response.data.count('ruben') == 0 and response.status_code == 200

    ###################################################
    ########   INTERNAl Tests
    ###################################################

    def test_check_add_action_data(self):
        """ Test if action data check is working well"""
        json_example_action = [{
            "action": "eu:c4a:usermotility:enter_bus",
            "location": "it:puglia:lecce:bus:39",
            "payload": {
                "user": "eu:c4a:pilot:madrid:user:12346",
                "position": "urn:ogc:def:crs:EPSG:6.6:4326"
            },
            "timestamp": "2014-05-20 07:08:41.22222",
            "rating": 0.1,
            "extra": {
                "pilot": "lecce"
            },
            "secret": "jwt_token"
        }]

        self.assertTrue(api._check_add_action_data(json_example_action))

    def test_check_add_risk_data(self):
        """ Test if risk data check is working well"""
        json_example_risk = [{
            "risk_name": "Lose your head",
            "ratio": 0.3,
            "description": "This is a risk description"
        }]

        self.assertTrue(api._check_add_risk_data(json_example_risk))

    def test_check_add_activity_data(self):
        """ Test if activity data check is working well"""
        json_example_activity = [{
            "activity_name": "Make breakfast"
        }]

        self.assertTrue(api._check_add_activity_data(json_example_activity))

    def test_check_add_new_user(self):
        """ Test if the add new user check is working well"""
        json_example_user = [{
            "username": "rmulero",
            "password": "heyPassWord1212323@@@#@3!!",
            "type": "admin"
        }]

        self.assertTrue(api._check_add_new_user(json_example_user))

    def test_check_search(self):
        """ Test if search check is working well"""
        json_example_search = {
            'table': 'user_in_system',
            'criteria': {
                "col1": "value",
                "col2": "value"
            },
            ###### Optional parameters
            'limit': 2323,
            'offset': 2,
            'order_by': 'desc'
        }

        self.assertTrue(api._check_search(json_example_search))


# todo add data test when we have Datbase logic finished

if __name__ == '__main__':
    unittest.main()
