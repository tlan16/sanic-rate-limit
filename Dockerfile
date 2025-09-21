FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync

COPY . .
ENTRYPOINT []
CMD ["uv", "run", "main.py"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=1s --retries=3 \
  CMD status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000) && \
      ([ "$status" = "200" ] || [ "$status" = "429" ]) || exit 1
