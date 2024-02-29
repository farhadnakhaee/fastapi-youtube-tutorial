from django.contrib.auth import get_user_model
from django.db import models
from .digikala_api import DigikalaAPI

digikala_api = DigikalaAPI()
User = get_user_model()


class Presentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    presenter_name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    present_date = models.CharField(max_length=255, default="زمستان ۱۴۰۱")
    background_image = models.ImageField(upload_to="background_image")
    slug = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.slug

    class Meta:
        app_label = "presentation"


class Slide(models.Model):
    data = models.JSONField(null=True)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='slides')
    order = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.url
        
    class Meta:
        ordering = ('order',)
        app_label = "presentation"
