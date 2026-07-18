from django.shortcuts import render, get_object_or_404
from .models import Menu  # Modelingizni chaqirib olamiz

def Home(request):
    menyular = Menu.objects.all()

    # Ma'lumotlarni HTML faylga 'menyular' degan nom bilan uzatamiz
    return render(request, 'menu/index.html', {'menyular': menyular})

def Menu_detail(request,pk):
    taom = get_object_or_404(Menu, id=pk)
    return render(request,'menu/detail.html', {'taom': taom })
