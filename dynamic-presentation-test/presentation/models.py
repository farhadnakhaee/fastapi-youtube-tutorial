from django.db import models
from django.contrib.auth import get_user_model
from .digikala_api import DigikalaAPI

digikala_api = DigikalaAPI()

User = get_user_model()


class Url(models.Model):
    url = models.CharField(max_length=255)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.url
    
    def fetch_data(self):
        if self.data:
            return self.data

        data = digikala_api.get_section(self.url)

        self.data = data
        self.save()

        return data


class Presentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    presenter_name = models.CharField(max_length=255)
    date = models.DateField()
    background_image = models.ImageField(upload_to='background_image', 
                                         default='presentation-background-1.jpg')
    slug = models.CharField(max_length=255)
    urls = models.ManyToManyField(Url)

    def __str__(self) -> str:
        return self.slug


        