FROM python:3.11-slim

RUN adduser --disabled-password appuser
USER appuser

WORKDIR /app
COPY api/ .
RUN pip install --no-cache-dir flask bcrypt

EXPOSE 5000
CMD ["python", "app.py"]