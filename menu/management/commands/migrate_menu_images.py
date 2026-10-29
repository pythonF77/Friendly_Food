from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from menu.models import Menu


class Command(BaseCommand):
    help = 'Upload existing local menu images to the configured persistent media storage.'

    def handle(self, *args, **options):
        if not settings.CLOUDINARY_CONFIGURED:
            raise CommandError(
                'Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and '
                'CLOUDINARY_API_SECRET before running this command.'
            )

        local_media = FileSystemStorage(location=Path(settings.BASE_DIR) / 'media')
        moved = 0
        missing = 0

        for item in Menu.objects.iterator():
            old_name = item.image.name.replace('\\', '/') if item.image else ''
            if not old_name:
                old_name = f'menu_images/{slugify(item.name)}.jpg'
            if default_storage.exists(old_name):
                if not item.image:
                    item.image.name = old_name
                    item.save(update_fields=['image'])
                continue
            if not local_media.exists(old_name):
                if item.image:
                    self.stderr.write(f'Missing local image for menu item: {item.pk} ({old_name})')
                missing += 1
                continue

            with local_media.open(old_name, 'rb') as image_file:
                new_name = default_storage.save(old_name, ContentFile(image_file.read()))
            item.image.name = new_name
            item.save(update_fields=['image'])
            moved += 1

        self.stdout.write(self.style.SUCCESS(f'Uploaded {moved} images; {missing} local files were missing.'))
