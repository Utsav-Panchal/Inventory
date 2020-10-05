import unittest

try:
    from app import app
except Exception as e:
    print("Exception has generated: ", e)


class FlaskTest(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/stores")
        statuscode = response.status_codes
        self.assertEqual(statuscode, 200)

    # content Check
    def test_index_content(self):
        tester = app.test_client(self)
        response = response = tester.get("/stores")
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()