from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    def image_path(self):
        return f'{self.user.id}/profile_pics'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default/profile_pics/default.jpg', upload_to=image_path)

    def __str__(self):
        return f'{self.user.username} Profile'