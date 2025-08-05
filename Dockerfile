# Use official Python 3.10 slim image (includes imghdr)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose port (not actually used; polling bot)
EXPOSE 8000

# Launch your bot
CMD ["python", "main.py"]
