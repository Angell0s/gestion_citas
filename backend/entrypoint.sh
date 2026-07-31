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

echo "Verificando/Iniciando datos iniciales (Superusuario)..."
python -m app.db.init_db

echo "Iniciando FastAPI..."
exec "$@"