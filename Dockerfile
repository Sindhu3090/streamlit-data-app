# [SOLUTION]
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# install curl for healthcheck
RUN apt-get update && apt-get install -y curl

# Copy dependency files first so this layer is cached when only app code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Then copy the application code.
COPY . .

EXPOSE 8501

# ✅ Challenge 2: Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
# [/SOLUTION]
