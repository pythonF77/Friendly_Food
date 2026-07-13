version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: dostlik_postgres_server
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=dostlik_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1111
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: dostlik_django_server
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_NAME=dostlik_db
      - DB_USER=postgres
      - DB_PASSWORD=1111
      - DB_HOST=db
      - DB_PORT=5432

volumes:
  postgres_data: