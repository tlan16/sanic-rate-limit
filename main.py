import os
from functools import lru_cache
# noinspection PyProtectedMember
from multiprocessing.managers import DictProxy
from typing import cast

from sanic import Sanic, Request
from sanic.response import text, json

from config import get_config
from multiprocessing import Manager

app = Sanic("rate_limit_demo")
config = get_config()

RateCounter = DictProxy[str, int]

@app.get("/")
async def hello_world(request: Request):
    if config.APP_DEBUG:
        worker_id = os.getpid()
        lookup_key = str(worker_id)
        print(f"Lookup key: {lookup_key}")
        rate_counter = cast(RateCounter, request.app.shared_ctx.rate_counter)
        rate_counter[lookup_key] = rate_counter.get(lookup_key, 0) + 1
        return json({
            "worker_id": os.getpid(),
            "queue": dict(rate_counter),
        })
    return text("OK")

@lru_cache(maxsize=1)
def get_number_of_workers() -> int:
    if config.APP_WORKERS is not None:
        if config.APP_DEBUG:
            print(f"Using {config.APP_WORKERS} worker(s) from env var APP_WORKERS")
        return config.APP_WORKERS

    number_of_cpus = os.cpu_count() or 1
    number_of_cpus = max(1, number_of_cpus)
    if config.APP_DEBUG:
        print(f"Using {number_of_cpus} worker(s) based on CPU count")
    return number_of_cpus


@app.main_process_start
async def main_process_start(app_to_start: Sanic):
    manager = Manager()
    rate_counter: RateCounter = manager.dict()
    app_to_start.shared_ctx.rate_counter = rate_counter


def main():
    app.run(
        workers=get_number_of_workers(),
    )


if __name__ == "__main__":
    main()
