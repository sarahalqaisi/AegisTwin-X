FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="AegisTwin X" \
      org.opencontainers.image.description="Defensive product-security intelligence portfolio" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY pyproject.toml ./
COPY aegistwin ./aegistwin
RUN pip install --no-cache-dir .
COPY policies ./policies
COPY web ./web
RUN mkdir -p /app/data && useradd --create-home --uid 10001 aegis && chown -R aegis:aegis /app
USER aegis
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"
CMD ["uvicorn", "aegistwin.main:app", "--host", "0.0.0.0", "--port", "8000"]
