"""
    Test suites for the REST API.
"""
import unittest
import json
import requests


class PiGlowTestCase(unittest.TestCase):

    def tearDown(self):
        r = requests.put('http://localhost:5000/patterns/clear')

    def test_arms(self):
        for i in range(1, 4):
            for b in range(255, -1, -1):
                data = {'brightness': b}
                r = requests.put('http://localhost:5000/arms/%d' % i, data)
                self.assertEqual(r.status_code, 200)

    def test_single_leds(self):
        for i in range(1, 19):
            for b in range(255, -1, -1):
                data = {'brightness': b}
                r = requests.put('http://localhost:5000/leds/%d' % i, data)
                self.assertEqual(r.status_code, 200)

    def test_colors(self):
        for i in range(1, 7):
            for b in range(255, -1, -1):
                data = {'brightness': b}
                r = requests.put('http://localhost:5000/colors/%d' % i, data)
                self.assertEqual(r.status_code, 200)

    def test_bad_arms(self):

        for i in [-1, 0, 4, 5, 6]:
            data = {'brightness': 100}
            r = requests.put('http://localhost:5000/arms/%d' % i, data)
            self.assertEqual(r.status_code, 404, 'out of range arm id')

        for i in range(1, 4):
            for b in [-2, -1, 256, 257]:
                data = {'brightness': b}
                r = requests.put('http://localhost:5000/arms/%d' % i, data)
                self.assertEqual(r.status_code, 400, 'out of range brightness')

    def test_bad_leds(self):

        for i in [-1, 0, 19, 20]:
            data = {'brightness': 100}
            r = requests.put('http://localhost:5000/leds/%d' % i, data)
            self.assertEqual(r.status_code, 404, 'out of range LED id')

        for i in range(1, 19):
            for b in [-2, -1, 256, 257]:
                data = {'brightness': b}
                r = requests.put('http://localhost:5000/leds/%d' % i, data)
                self.assertEqual(r.status_code, 401, 'out of range brightness')

    def test_group_leds(self):
        """ Test simultanous LED updates. """
        data = []
        b = 1
        for i in range(1, 19):
            data.append({'led_id': i, 'brightness': b})
            b += 10
        print data
        r = requests.put('http://localhost:5000/leds', data=json.dumps(data),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
