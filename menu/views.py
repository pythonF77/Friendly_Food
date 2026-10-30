from uuid import uuid4

from django import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.utils.text import slugify
from .models import Menu, MenuComment, MenuReaction


class MenuCommentForm(forms.ModelForm):
    class Meta:
        model = MenuComment
        fields = ("name", "body")
        labels = {"name": "Ismingiz", "body": "Fikringiz"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Masalan, Dilnoza", "autocomplete": "name"}),
            "body": forms.Textarea(attrs={"placeholder": "Taom haqida fikringizni yozing", "rows": 4, "maxlength": 1200}),
        }


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
    visitor_key = request.session.get("menu_visitor_key")
    if not visitor_key:
        visitor_key = str(uuid4())
        request.session["menu_visitor_key"] = visitor_key

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "react":
            reaction = request.POST.get("reaction")
            if reaction in (MenuReaction.LIKE, MenuReaction.DISLIKE):
                MenuReaction.objects.update_or_create(
                    menu=taom, visitor_key=visitor_key, defaults={"reaction": reaction}
                )
                messages.success(request, "Fikringiz qabul qilindi.")
            else:
                messages.error(request, "Reaksiyani tanlang.")
        elif action == "comment":
            comment_form = MenuCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.menu = taom
                comment.name = comment.name.strip() or "Mehmon"
                comment.body = comment.body.strip()
                comment.save()
                messages.success(request, "Fikringiz qo‘shildi. Rahmat!")
                return redirect(f"{request.path}#comments")
            messages.error(request, "Fikrni yuborishdan oldin maydonlarni tekshiring.")
        return redirect(f"{request.path}#feedback")

    context = {
        "taom": taom,
        "comment_form": MenuCommentForm(),
        "comments": taom.comments.all(),
        "like_count": taom.reactions.filter(reaction=MenuReaction.LIKE).count(),
        "dislike_count": taom.reactions.filter(reaction=MenuReaction.DISLIKE).count(),
        "user_reaction": MenuReaction.objects.filter(menu=taom, visitor_key=visitor_key).values_list("reaction", flat=True).first(),
    }
    return render(request, 'menu/detail.html', context)
