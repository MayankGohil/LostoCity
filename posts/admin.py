from django.contrib import admin
from .models import ItemLost, ItemFound, ItemClaim, ItemReturn, Post

# Register your models here.
admin.site.register(ItemLost)
admin.site.register(ItemFound)
admin.site.register(ItemClaim)
admin.site.register(ItemReturn)
admin.site.register(Post)