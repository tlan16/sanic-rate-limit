import random
import string
import unittest
import urllib.request
from urllib.error import HTTPError, URLError


def generate_random_client_id() -> str:
    suffix =  ''.join(random.choice(
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
    ) for _ in range(16))
    return f"test-client-{suffix}"

class TestMain(unittest.TestCase):
    def test_happy_path(self):
        response = make_request(generate_random_client_id())
        self.assertEqual(response.status, 200)

    def test_rate_limited_with_one_client(self):
        client_id = generate_random_client_id()
        # assert first request is successful
        self.assertEqual(make_request(client_id).status, 200)
        # assert one of subsequent requests are rate limited
        with self.assertRaises(HTTPError) as cm:
            for _ in range(1000):
                make_request("test-client-01")
        self.assertEqual(cm.exception.code, 429)

    def test_rate_limited_with_multiple_clients(self):
        client_ids = tuple(
            generate_random_client_id()
            for i in range(10)
        )
        for client_id in client_ids:
            # assert first request is successful
            self.assertEqual(make_request(client_id).status, 200)
            # assert one of subsequent requests are rate limited
            with self.assertRaises(HTTPError) as cm:
                for _ in range(1000):
                    make_request("test-client-01")
            self.assertEqual(cm.exception.code, 429)

def make_request(client_id: str):
    req = urllib.request.Request(
        "http://127.0.0.1:8000",
        headers={"X-Forwarded-For": client_id},
    )
    with urllib.request.urlopen(req) as resp:
        return resp

if __name__ == '__main__':
    unittest.main(verbosity=2)
