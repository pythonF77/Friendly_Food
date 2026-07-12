from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    class Meta:
        verbose_name= "Menyular"


    def __str__(self):
        return self.name