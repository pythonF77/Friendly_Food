from django.shortcuts import render, get_object_or_404
from .models import Menu

def Home(request):
    query = request.GET.get('q', '').strip()
    menyular = Menu.objects.all().order_by('name')
    if query:
        menyular = menyular.filter(name__icontains=query)

    return render(request, 'menu/index.html', {'menyular': menyular, 'query': query})

def Menu_detail(request, pk):
    taom = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/detail.html', {'taom': taom})
