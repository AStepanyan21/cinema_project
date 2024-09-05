echo "Running tests..."
pytest tests --asyncio-mode=auto

echo "Applying database migrations..."
alembic upgrade head

echo "Starting the server..."
HOST_PORT=${HOST_PORT:-8000}
exec uvicorn app.main:app --host 0.0.0.0 --port $HOST_PORT --reload
