First update .env file is you want, otherwise it's ready to be used without modification.

**(a) with docker:**

```shell
uv run 'scripts/benchmark.sh'
```

<details>
<summary>Example output:</summary>

```text
(sanic-rate-limit) ➜  sanic-rate-limit git:(main) ✗ ./scripts/benchmark.sh
Service 'dev' is not running. Starting...
Building dev service ...
[+] Running 2/2
 ✔ Network sanic-rate-limit_default  Created                                                            0.0s 
 ✔ Container sanic-rate-limit-dev-1  Healthy                                                            5.6s 
Generated 50 client IDs.
All status codes received: {200, 429}
status counts: {200: 100, 429: 67052}
Total requests made: 67152
Requests per second: 22384.00
[+] Running 2/2
 ✔ Container sanic-rate-limit-dev-1  Removed                                                            0.3s 
 ✔ Network sanic-rate-limit_default  Removed                                                            0.1s 
```
</details>

**(b) with local python interpreter** ([uv](https://github.com/astral-sh/uv) in this case):

```shell
uv run 'main.py'
```

Open another terminal session:

```shell
uv run 'benchmark.py'
```

(terminal the first terminal session if you want)
