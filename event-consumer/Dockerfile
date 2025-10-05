FROM python:3.10-slim

WORKDIR /worker

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (from current directory)
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /worker
USER appuser

CMD ["python", "consumer.py"]