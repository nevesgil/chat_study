FROM python:3.12-slim

WORKDIR /app

# install uv
RUN pip install uv

# copy dependency metadata first (better Docker caching)
COPY pyproject.toml uv.lock* ./

# install dependencies
RUN uv sync --frozen

# copy application code
COPY . .

CMD ["uv", "run", "--frozen", "uvicorn", "src.server.server:app", "--host", "0.0.0.0", "--port", "8000"]