# backend/entrypoint.sh
#!/bin/sh
set -e

echo "Esperando a PostgreSQL en db:5432..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL disponible."

echo "Aplicando migraciones..."
alembic upgrade head

echo "Iniciando FastAPI..."
exec "$@"