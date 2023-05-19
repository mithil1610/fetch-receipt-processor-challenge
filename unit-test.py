import unittest
import json
from app import app

class ReceiptProcessingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_points_with_valid_receipt_id(self):
        receipt_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                }
            ],
            "total": "9.00"
        }

        response = self.app.post('/receipts/process', json=receipt_data)
        data = json.loads(response.get_data(as_text=True))
        receipt_id = data['id']

        expected_response = {'points': 109 }

        response = self.app.get(f'/receipts/{receipt_id}/points')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected_response)

if __name__ == '__main__':
    unittest.main()
