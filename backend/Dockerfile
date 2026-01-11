FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configure poetry
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command is overridden by docker-compose for dev
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
