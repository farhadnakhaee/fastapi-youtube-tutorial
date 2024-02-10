from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Presentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    presenter_name = models.CharField(max_length=255)
    date = models.DateField()
    background_image = models.ImageField()

    def __str__(self) -> str:
        return self.title


class Slide(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    presentation = models.ForeignKey(Presentation, on_delete=models.PROTECT)