from sanic import Sanic
from sanic.response import text

app = Sanic("rate_limit_demo")

@app.get("/")
async def hello_world(_request):
    return text("OK")


def main():
    app.run()


if __name__ == "__main__":
    main()
