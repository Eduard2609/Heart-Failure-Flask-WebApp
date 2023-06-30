import unittest
from flaskheart import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_prediction_page(self):
        response = self.app.get('/prediction')
        self.assertEqual(response.status_code, 404)

    def test_history_page(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()