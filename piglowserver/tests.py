"""
    Test suites.
"""
import unittest
import requests


class ArmTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
