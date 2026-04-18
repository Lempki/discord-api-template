FROM python:3.12-slim
RUN useradd --create-home appuser
WORKDIR /app
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir .
USER appuser
CMD ["uvicorn", "api_template.main:app", "--host", "0.0.0.0", "--port", "8000"]
