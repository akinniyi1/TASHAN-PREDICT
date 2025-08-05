# Dockerfile
FROM python:3.10-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose any port (Render will detect the HTTP service)
EXPOSE 10000

# Start the bot (this will launch both FastAPI and the Telegram bot)
CMD ["python", "main.py"]
