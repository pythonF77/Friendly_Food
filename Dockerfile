# 1. Python-ning eng barqaror va mos versiyasini tanlaymiz
FROM python:3.12-slim

# 2. Terminalda loglar darhol ko'rinishi va ortiqcha fayllar yozilmasligi sozlamalari
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#
## 3. Konteyner ichidagi asosiy ishchi papkani belgilaymiz
WORKDIR /app
#
## 4. Tizim uchun kerakli qo'shimcha paketlarni o'rnatamiz (PostgreSQL bilan xatosiz ishlash uchun)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

## 5. requirements.txt faylini konteynerga nusxalaymiz va kutubxonalarni o'rnatamiz
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Loyihaning barcha fayllarini konteyner ichiga ko'chiramiz
COPY . /app/

# 7. Portni ochamiz
EXPOSE 10000

# Render PORT qiymatidan foydalanib, avval jadvallarni yangilaymiz.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec gunicorn my_admin.wsgi:application --bind 0.0.0.0:${PORT:-10000} --access-logfile - --error-logfile -"]
