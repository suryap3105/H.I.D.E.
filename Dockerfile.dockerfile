# --- Stage 1: Build Environment ---
# Use a slim Python base image
FROM python:3.10-slim as builder

# Set the working directory
WORKDIR /app

# Install system dependencies that might be needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies into a virtual environment within the builder
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Final Application Image ---
# Use the same slim Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code and adapters
COPY src/ ./src/
COPY adapters/ ./adapters/
COPY train.py .
COPY score.py .

# Set the PATH to include the virtual environment's binaries
ENV PATH="/opt/venv/bin:$PATH"

# Set the PYTHONPATH so Python can find the 'hide' module
ENV PYTHONPATH="${PYTHONPATH}:/app"

# The container will not run a server by default.
# It is designed to be used with `docker run` to execute the train/score scripts.
# See the README.md for usage examples.
CMD ["bash"]