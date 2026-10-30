from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    class Meta:
        verbose_name= "Menyular"


    def __str__(self):
        return self.name


class MenuReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    REACTION_CHOICES = [(LIKE, "Yoqdi"), (DISLIKE, "Yoqmadi")]

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="reactions")
    visitor_key = models.CharField(max_length=36)
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("menu", "visitor_key"), name="one_reaction_per_menu_visitor")]

    def __str__(self):
        return f"{self.menu}: {self.get_reaction_display()}"


class MenuComment(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=60, blank=True, default="")
    body = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.menu}: {self.body[:50]}"


