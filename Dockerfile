FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_PORT=8000

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libpq-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run_app.sh /app/run_app.sh
RUN chmod +x /app/run_app.sh

COPY . .

RUN ls -la /app

EXPOSE ${APP_PORT}

CMD ["/app/run_app.sh"]
