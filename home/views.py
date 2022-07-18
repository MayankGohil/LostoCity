from django.shortcuts import render
from posts.models import ItemLost, ItemFound, Post

# Create your views here.
#Home
def HomeView(request):
    context = {
        'objects': None,
    }
    posts = Post.objects.all().order_by('-id')[:4]
    obj = []
    for post in posts:
        container = []
        if post.itemLost:
            container.extend(["lost",post.itemLost])
        if post.itemFound:
            container.extend(["found",post.itemFound])
        obj.append(container)
    context['objects'] = obj
    return render(request, template_name='home/home.html', context=context)