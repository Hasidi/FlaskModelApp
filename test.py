import json
import os
import unittest
import requests

from src.model_provider import MODEL_FILE_PATH

port = os.environ.get('APP_PORT')
BASE_URL = f'http://localhost:{port}'


class SystemTests(unittest.TestCase):

    def test_model_upload(self):
        with open(MODEL_FILE_PATH, 'r') as f:
            data1 = f.read()
        modify_t1 = os.path.getmtime(MODEL_FILE_PATH)
        res = requests.post(url=f'{BASE_URL}/api/model',
                            data=data1,
                            headers={'Content-Type': 'text/plain'})
        modify_t2 = os.path.getmtime(MODEL_FILE_PATH)
        self.assertEqual(200, res.status_code)
        self.assertGreater(modify_t2, modify_t1)
        with open(MODEL_FILE_PATH, 'r') as f:
            data2 = f.read()
        self.assertEqual(data1, data2)

    def test_model_prediction(self):
        resp = requests.post(f'{BASE_URL}/api/prediction', json={"log": "some1"})
        self.assertEqual(200, resp.status_code)
        result = json.loads(resp.text)['result']
        self.assertEqual('5', result)




