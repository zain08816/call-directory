# Stage 1: build admin dashboard
FROM node:20-alpine AS frontend
WORKDIR /build

COPY admin/package.json admin/package-lock.json* ./
RUN npm ci

COPY admin/ ./
RUN npm run build

# Stage 2: run FastAPI app
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/
COPY legal/ ./legal/
COPY --from=frontend /build/dist ./admin/dist

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
