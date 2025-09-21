import os
from functools import lru_cache
# noinspection PyProtectedMember
from multiprocessing.managers import DictProxy
from time import perf_counter, time
from typing import cast

from sanic import Sanic, Request
from sanic.response import text, json

from config import get_config
from multiprocessing import Manager

app = Sanic("rate_limit_demo")
config = get_config()

LastRequestMinute = int
RequestCount = int
RateCounter = DictProxy[str, tuple[LastRequestMinute, RequestCount]]

rate_limit_fineness_seconds: float = 5.0

def get_current_minute() -> int:
    return int(time() // 60)

def is_rate_limited(rate_counter: RateCounter, lookup_key: str) -> bool:
    current_minutes = get_current_minute()
    dict_item = rate_counter.get(lookup_key)
    if config.APP_DEBUG:
        print(f"Worker {lookup_key} dict_item: {dict_item}")
    if dict_item is None:
        rate_counter[lookup_key] = (current_minutes, 1)
        if config.APP_DEBUG:
            print(
                f"Worker {lookup_key} initialized rate counter."
                f" 1/{get_config().RATE_LIMIT_REQ_PER_MIN}"
            )
        return False

    last_request_minute, count = dict_item
    if last_request_minute == current_minutes:
        new_count = count + 1
        rate_counter[lookup_key] = (last_request_minute, new_count)
        reached_limit = new_count > config.RATE_LIMIT_REQ_PER_MIN
        if config.APP_DEBUG:
            print(
                f"Worker {lookup_key} incremented rate counter to {new_count}," 
                f" reached_limit={reached_limit}."
                f" {new_count}/{get_config().RATE_LIMIT_REQ_PER_MIN}"
            )
        return reached_limit

    rate_counter[lookup_key] = (current_minutes, 1)
    if config.APP_DEBUG:
        print(
            f"Worker {lookup_key} reset rate counter for new minute"
            f" 1/{get_config().RATE_LIMIT_REQ_PER_MIN}"
        )
    return False

def compute_lookup_key(request: Request) -> str:
    ## For demo purpose I'll use the http header "X-Forwarded-For" for requestor IP
    lookup_key = request.headers.get("X-Forwarded-For", request.ip)
    assert isinstance(lookup_key, str) and len(lookup_key) > 0
    return lookup_key

@app.get("/")
async def hello_world(request: Request):
    lookup_key = compute_lookup_key(request)
    rate_counter = cast(RateCounter, request.app.shared_ctx.rate_counter)
    reached_limit= is_rate_limited(
        rate_counter,
        lookup_key,
    )
    if reached_limit:
        return text("429 Too Many Requests", status=429)

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
