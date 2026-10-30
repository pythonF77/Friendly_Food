"""Create a first Django admin account from environment variables."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_admin.settings")
django.setup()

from django.contrib.auth import get_user_model


def main():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
    if not username or not email or not password:
        print("Admin setup skipped; Django superuser environment variables are not set.")
        return

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True, "is_active": True},
    )
    if not created:
        print("Admin account already exists; leaving its password and permissions unchanged.")
        return

    user.set_password(password)
    user.save(update_fields=["password"])
    print("Admin account created.")


if __name__ == "__main__":
    main()
