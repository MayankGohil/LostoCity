from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ItemLost(models.Model):
    def image_path(self):
        return f'{self.user.id}/item_lost_images'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.ImageField(default='default/item_lost_images/default.jpg', upload_to=image_path)
    active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} lost {self.name}'

class ItemFound(models.Model):
    def image_path(self):
        return f'{self.user.id}/item_found_images'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.ImageField(default='default/item_found_images/default.jpg', upload_to=image_path)
    active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} found {self.name}'

class ItemClaim(models.Model):
    def image_path(self):
        return f'{self.user.id}/item_claim_images'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemFound, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.ImageField(default='default/item_claim_images/default.jpg', upload_to=image_path)
    accepted = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} claims {self.item}'

class ItemReturn(models.Model):
    def image_path(self):
        return f'{self.user.id}/item_return_images'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemLost, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.ImageField(default='default/item_return_images/default.jpg', upload_to=image_path)
    accepted = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} wants to return {self.item}'

class Post(models.Model):
    itemLost = models.OneToOneField(ItemLost, on_delete=models.CASCADE,null=True, blank=True)
    itemFound = models.OneToOneField(ItemFound, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} posted'