# Base image
FROM python:3.14-slim-bookworm

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency definitions first (better build caching)
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the project
COPY src ./src
COPY models ./models

# Expose API port
EXPOSE 8000

# Start the API
CMD ["poetry", "run", "uvicorn", "hybrid_cse_system_v2.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
