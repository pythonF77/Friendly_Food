from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.utils.text import slugify
from .models import Menu


MENU_IMAGE_FALLBACKS = {
    "beshtekis": "beshtekis.jpg",
    "mastava": "mastava.jpg",
    "manti": "manti-dona.jpg",
    "osh-devzira": "devzira-osh.jpg",
    "osh-lavzer": "osh-lazer.jpg",
    "qotirma": "qotirma.jpg",
    "qovirma-lagman": "qovurma-lagman.jpg",
    "birzol": "birizol.jpg",
    "bistirogen": "bistrogen.jpg",
    "galipsa-shorva": "galipsa-shorva.jpg",
    "gosht-qovurdoq-100gr": "gosht-qovurdoq-100gr.jpg",
    "gulyash": "gulyash.jpg",
    "kfs-100gr": "kfs-100gr.jpg",
    "lagman": "uygur-lagman.jpg",
    "langet": "langet.jpg",
    "shorva-xal-xal": "xal-xal-shorva.jpg",
}


def _set_fallback_image(item):
    image_name = MENU_IMAGE_FALLBACKS.get(slugify(item.name))
    item.fallback_image_url = static(f"menu/images/dishes/{image_name}") if image_name else ""
    return item


def Home(request):
    query = request.GET.get('q', '').strip()
    menyular = Menu.objects.all().order_by('name')
    if query:
        menyular = menyular.filter(name__icontains=query)
    menyular = [_set_fallback_image(item) for item in menyular]

    return render(request, 'menu/index.html', {'menyular': menyular, 'query': query})

def Menu_detail(request, pk):
    taom = get_object_or_404(Menu, pk=pk)
    _set_fallback_image(taom)
    return render(request, 'menu/detail.html', {'taom': taom})
