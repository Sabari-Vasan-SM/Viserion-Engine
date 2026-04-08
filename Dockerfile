FROM python:3.10-slim

# Install necessary system libraries for image processing
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the AI model during the Docker build.
# This prevents the server from hanging/timing out on Render when the first request hits!
RUN python -c "from rembg import new_session; new_session('u2net')"

# Copy the rest of the application
COPY . .

# Run the Uvicorn server, using the PORT environment variable provided by Render
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
