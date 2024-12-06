FROM python:3.12.1-alpine AS builder

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.12.1-alpine

WORKDIR /app

COPY --from=builder /app/wheels /wheels

COPY --from=builder /app/requirements.txt .

RUN apk add --no-cache libffi-dev && \
    pip install --no-cache /wheels/**

COPY . .

CMD ["python", "main.py"]
