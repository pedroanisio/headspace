FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY pyproject.toml uv.lock ./

# Install UV for faster dependency management
RUN pip install uv

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 