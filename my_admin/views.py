import secrets

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


User = get_user_model()


class AdminSetupForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=False)
    setup_token = forms.CharField(
        label="Bir martalik maxfiy kod",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "off"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {"username": "Foydalanuvchi nomi"}

    def clean_setup_token(self):
        submitted = self.cleaned_data["setup_token"]
        configured = settings.ADMIN_SETUP_TOKEN
        if not configured or not secrets.compare_digest(submitted, configured):
            raise forms.ValidationError("Maxfiy kod noto‘g‘ri.")
        return submitted

    def clean(self):
        cleaned = super().clean()
        if User.objects.filter(is_superuser=True).exists():
            raise forms.ValidationError("Admin akkaunti allaqachon yaratilgan.")
        if "password1" in cleaned:
            validate_password(cleaned["password1"])
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


def setup_admin(request):
    if not settings.ADMIN_SETUP_TOKEN:
        return HttpResponse("Admin sozlash sahifasi yopiq.", status=404)

    if User.objects.filter(is_superuser=True).exists():
        return render(request, "admin_setup_closed.html", status=410)

    form = AdminSetupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            if User.objects.filter(is_superuser=True).exists():
                return render(request, "admin_setup_closed.html", status=410)
            form.save()
        return render(request, "admin_setup_success.html")

    return render(request, "admin_setup.html", {"form": form})
