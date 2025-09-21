import os
from functools import lru_cache

from sanic import Sanic
from sanic.response import text

from config import get_config

app = Sanic("rate_limit_demo")
config = get_config()

@app.get("/")
async def hello_world(_request):
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


def main():
    app.run(
        workers=get_number_of_workers()
    )


if __name__ == "__main__":
    main()
