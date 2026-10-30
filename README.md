# Do‘stlik oshxonasi

Django asosidagi o‘zbekcha oshxona menyusi va taomlarni boshqarish uchun admin paneli.

## Render’ga joylash

Loyiha Render Docker web service uchun tayyorlangan. Render’dagi mavjud PostgreSQL bazasini saqlab qolish uchun yangi baza yaratish shart emas.

Web service sozlamalarida quyidagi muhit o‘zgaruvchilarini kiriting:

| Nomi | Qiymati |
| --- | --- |
| `DATABASE_URL` | Mavjud Render PostgreSQL bazasining connection URL’i. Web service bilan bir regionda bo‘lsa, Internal URL’dan foydalaning. |
| `SECRET_KEY` | Yangi, maxfiy Django kaliti. Render Dashboard’da Generate ishlating. |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Sayt hostlari, masalan `friendly-food.onrender.com,www.example.uz` — `https://` yozilmaydi. |
| `CSRF_TRUSTED_ORIGINS` | Shu hostlar to‘liq manzil bilan, masalan `https://friendly-food.onrender.com,https://www.example.uz`. |

Docker deploy’da `Dockerfile` Python 3.12’dan foydalanadi. Har ishga tushishda migratsiyalar qo‘llanadi, static fayllar yig‘iladi va Gunicorn Render bergan `PORT`’da ishga tushadi. GitHub repozitoriyingizda Django loyihasi ildiz papkada joylashgan.

Agar Render’da Native Python service ishlatayotgan bo‘lsangiz:

- Build command: `bash build.sh`
- Start command: `gunicorn my_admin.wsgi:application --bind 0.0.0.0:$PORT`
- `.python-version` Django 6 bilan mos Python 3.12 versiyasini belgilaydi.

## Admin paneliga kirish

Manzil: `https://sayt-manzili/admin/`

Render Dashboard’dan web service Shell’ini ochib, bir marta migratsiya va admin hisobini yarating:

```sh
python manage.py migrate --noinput
python manage.py createsuperuser
```

`createsuperuser` sizdan login, email va parolni so‘raydi. Bu buyruq Render’dagi `DATABASE_URL` orqali mavjud bazaga ulanadi. Admin hisobi bazada oldindan bo‘lsa, yangisini yaratish shart emas.

## Taom rasmlari

Render’ning odatiy fayl tizimi qayta deploy yoki restartdan keyin o‘zgarishi mumkin. Admin orqali keyinchalik yuklanadigan rasmlarni saqlash uchun web service’ga persistent disk ulab, `MEDIA_ROOT`’ni disk yo‘liga qo‘ying yoki quyidagi uchta Cloudinary qiymatini Render Environment’ga qo‘shing: `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`. Uchtalasi sozlansa, loyiha Cloudinary media storage’dan foydalanadi. Mavjud mahalliy rasm fayllarini ko‘chirish uchun fayllar serverda mavjudligini tekshirib, Render Shell’da `python manage.py migrate_menu_images` buyrug‘ini bir marta bajaring. Bu buyruq bazadagi rasm yo‘llarini yangilaydi.

## Mahalliy ishga tushirish

Python 3.12 yoki yangirog‘ini o‘rnating, paketlarni `pip install -r requirements.txt` orqali o‘rnating va quyidagi muhit o‘zgaruvchilarini bering:

```text
DEBUG=True
SECRET_KEY=faqat-mahalliy-ishlatish-uchun-kalit
```

So‘ng `python manage.py migrate` va `python manage.py runserver` buyruqlarini bajaring. Mahalliy rejimda `DATABASE_URL` berilmasa, loyiha `db.sqlite3`’dan foydalanadi.

## Muhim xavfsizlik eslatmasi

Arxivdagi eski sozlamalarda Django kaliti va PostgreSQL connection ma’lumoti kod ichida saqlangan. Ularni Render Dashboard’da yangilang: yangi `SECRET_KEY` yarating, PostgreSQL parolini almashtiring va yangilangan connection URL’ni `DATABASE_URL`’ga qo‘ying. Eski `admin/admin` hisobini yaratadigan standart qiymatlar olib tashlandi.
