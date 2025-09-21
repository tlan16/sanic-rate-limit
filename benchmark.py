import asyncio
import random
import string
import sys

import aiohttp

URL = "http://localhost:8000"
POOL_SIZE = 50
CONCURRENCY = 20
DURATION_SECONDS = 3  # How long to run the benchmark


def generate_random_client_id() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(64))
    return f"test-client-{suffix}"


async def worker(
    session: aiohttp.ClientSession, client_ids: set[str], results: list[int], stop_event: asyncio.Event
) -> None:
    while not stop_event.is_set():
        client_id = random.choice(tuple(client_ids))
        try:
            async with session.get(URL, headers={"X-Forwarded-For": client_id}) as resp:
                status = resp.status
                results.append(status)
                if status not in (200, 429):
                    print(f"Unexpected status: {status}")
                    stop_event.set()
                    return
        except Exception as e:
            print(f"Request failed: {e}")
            stop_event.set()
            return


async def main() -> None:
    client_ids = set(generate_random_client_id() for _ in range(POOL_SIZE))
    print(f"Generated {len(client_ids)} client IDs.")

    results = []
    stop_event = asyncio.Event()

    async with aiohttp.ClientSession() as session:
        # Launch workers
        tasks = [worker(session, client_ids, results, stop_event) for _ in range(CONCURRENCY)]

        # Stop after duration
        asyncio.get_event_loop().call_later(DURATION_SECONDS, stop_event.set)

        await asyncio.gather(*tasks, return_exceptions=True)

    print(f"All status codes received: {set(results)}")
    print(f"status counts: { {code: results.count(code) for code in set(results)} }")
    print(f"Total requests made: {len(results)}")
    print(f"Requests per second: {len(results) / DURATION_SECONDS:.2f}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)
