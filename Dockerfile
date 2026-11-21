# ========================================================================
# PranaAI (प्राण AI) — Production Container
# Hardened, lightweight, non-root execution for Cloud Run & Container Runtimes
# ========================================================================

FROM python:3.12-slim

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install minimal OS dependencies for health checking
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run as non-root user for enterprise security
RUN adduser --disabled-password --gecos "" pranauser && \
    chown -R pranauser:pranauser /app
USER pranauser

# Expose server port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Launch application server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
