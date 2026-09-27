import os
import django

# Django muhitini sozlash (loyihangiz nomini yozing, masalan: my_admin.settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_admin.settings')
django.setup()

from django.contrib.auth.models import User

# O'zingiz xohlagan login, email va parolni shu yerga yozing
username = 'admin'
email = 'admin@gmail.com'
password = 'admin'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser muvaffaqiyatli yaratildi!")
else:
    print("Bu foydalanuvchi allaqachon mavjud!")