This is an interview code for a python, cpp project.

The interviewer provided:

> FTS is very computer science theory heavy, and its execution is on the other hand complex on engineering side
> https://sanic.dev/en/

> Sanic User Guide - The lightning-fast asynchronous Python web frame...
Sanic is a Python 3.9+ web server and web framework that's written to go fast.
This is the python framework that  I'm using for everything. Take it and implement / endpoint with rate limiting.
Your tests need to include a benchmark up to 100 r/s (this should be minimum performance on all cores of an average cpu)

> How you implement it is part of engineering know-how challenge (feel free to surprise me), keep in mind that prod deployment, including your benchmark, will spawn multiple processes to take advantage of all cores.

> Rate limiting should be based on a keyword (ip would be the most common one, but I usually limit things like queries too)

---

First update [.env](/.env) file is you want, otherwise it's ready to be used without modification.

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
