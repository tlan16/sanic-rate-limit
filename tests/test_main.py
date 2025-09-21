import random
import string
import sys
import unittest
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from urllib.response import addinfourl


def generate_random_client_id() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
    return f"test-client-{suffix}"


class TestMain(unittest.TestCase):
    def test_happy_path(self) -> None:
        response = make_request(generate_random_client_id())
        self.assertEqual(response.status, 200)

    def test_rate_limited_with_one_client(self) -> None:
        from config import get_config

        client_id = generate_random_client_id()
        for _ in range(get_config().RATE_LIMIT_REQ_PER_MIN):
            self.assertEqual(make_request(client_id).status, 200)
        with self.assertRaises(HTTPError) as cm:
            make_request(client_id)
        self.assertEqual(cm.exception.code, 429)

    def test_rate_limited_with_multiple_clients(self) -> None:
        from config import get_config

        client_ids = tuple(generate_random_client_id() for i in range(10))
        for client_id in client_ids:
            # assert first request is successful
            for _ in range(get_config().RATE_LIMIT_REQ_PER_MIN):
                self.assertEqual(make_request(client_id).status, 200)
            # assert one of subsequent requests are rate limited
            with self.assertRaises(HTTPError) as cm:
                make_request(client_id)
            self.assertEqual(cm.exception.code, 429)


def make_request(client_id: str) -> addinfourl:
    req = urllib.request.Request(
        "http://localhost:8000",
        headers={"X-Forwarded-For": client_id},
    )
    with urllib.request.urlopen(req) as resp:
        return resp


if __name__ == "__main__":
    project_directory = Path(__file__).parents[1]
    sys.path.append(str(project_directory.resolve()))
    unittest.main(verbosity=2)
