import unittest
from app_teste import app  # assuming your main Flask app is in `app.py`

class SubmitDataTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True

    def test_submit_data_success(self):
        # Simulated form data
        form_data = {
            'name': 'Test User',
            'ccnif': '123456789',
            'dependents': '1',
            'tenure': '12',
            'internetService': 'Fiber optic',
            'onlineSecurity': 'Yes',
            'techSupport': 'No',
            'contract': 'Month-to-month',
            'paperlessBilling': 'Yes',
            'paymentMethod': 'Credit card (automatic)',
            'monthlyCharges': '89.5',
            'churn': 'No'
        }

        response = self.app.post('/submit-data', data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 Redirect expected

        # Confirm it redirects to /contribuir
        self.assertIn('/contribuir', response.location)


    def test_submit_data_missing_fields(self):
        # Incomplete form data
        form_data = {
            'name': 'Test User',
            # missing 'ccnif' and others
        }

        response = self.app.post('/submit-data', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # You can check behavior for missing fields, but your current /submit-data doesn't enforce validation for required fields.
        # So it would still redirect — you could enhance this later.

if __name__ == '__main__':
    unittest.main()
