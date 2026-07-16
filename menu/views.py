from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Menu  # Modelingizni chaqirib olamiz
from django.contrib.auth.models import User
def Home(request):
    # 👇 VAQTINCHALIK ADMIN YARATISH KODI (Buni qo'shing)
    if not User.objects.filter(username="dostlik_admin").exists():
        User.objects.create_superuser("dostlik_admin", "admin@gmail.com", "Dostlik2026")
    # 👆 KOD TUGADI

    menyular = Menu.objects.all()

    # Ma'lumotlarni HTML faylga 'menyular' degan nom bilan uzatamiz
    return render(request, 'menu/index.html', {'menyular': menyular})

def Menu_detail(request,pk):
    taom = get_object_or_404(Menu, id=pk)
    return render(request,'menu/detail.html', {'taom': taom })
