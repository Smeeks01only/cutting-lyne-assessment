FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only torch to save massive amounts of space and RAM
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the Hugging Face model at build time so it doesn't download on every startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of the application
COPY . .

# Render dynamically assigns a port via the PORT env var. 
# Hugging Face Spaces defaults to 7860. This handles both!
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}
