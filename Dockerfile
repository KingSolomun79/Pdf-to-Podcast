# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg

# Copy the rest of the application code to the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port that FastAPI will run on
EXPOSE 8005

# Run the FastAPI application
CMD ["uvicorn", "fast_api_app:app", "--host", "0.0.0.0", "--port", "8005"]
