# Multi-arch base: python:3.12-slim publishes both linux/amd64 and linux/arm64,
# and all Python deps here ship wheels for both, so this image builds cleanly for
# either platform. Use `docker buildx --platform linux/amd64,linux/arm64` to publish
# a manifest list that runs on any candidate's cluster (see README).
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]
