from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import ItemLost, ItemFound, ItemClaim, ItemReturn, Post
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from app.settings import MEDIA_ROOT
import datetime

# Create your views here.
#Posts/Global Lost and Found List
def PostsView(request):
    context = {
        'objects': None,
        'posts': True,
    }
    posts = Post.objects.all().order_by('-id')
    obj = []
    for post in posts:
        container = []
        if post.itemLost:
            container.extend(["lost",post.itemLost])
        if post.itemFound:
            container.extend(["found",post.itemFound])
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Specific Posts
def SpecificPostsView(request, option):
    context = {
        'objects': None,
        'specificPosts': True,
    }
    posts = Post.objects.all().order_by('-id')
    obj = []
    for post in posts:
        container = []
        if post.itemLost and post.itemLost.category == option:
            container.extend(["lost",post.itemLost])
        if post.itemFound and post.itemFound.category == option:
            container.extend(["found",post.itemFound])
        if len(container):
            obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Global Lost List
def LostListView(request):
    context = {
        'ojects': None,
        'lostList': True,
    }
    items = ItemLost.objects.all().order_by('-id')
    obj = []
    for item in items:
        container = ['lost', item]
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Global Found List
def FoundListView(request):
    context = {
        'ojects': None,
        'foundList': True,
    }
    items = ItemFound.objects.all().order_by('-id')
    obj = []
    for item in items:
        container = ['found', item]
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Personal Posts/Personal Lost and Found List
@login_required
def MyPostsView(request):
    context = {
        'objects': None,
        'myPosts': True,
    }
    posts = Post.objects.filter(user=request.user).order_by('-id')
    obj = []
    for post in posts:
        container = []
        if post.itemLost:
            container.extend(["lost",post.itemLost])
        if post.itemFound:
            container.extend(["found",post.itemFound])
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Personal Lost List
@login_required
def MyLostListView(request):
    context = {
        'ojects': None,
        'myLostList': True,
    }
    items = ItemLost.objects.filter(user=request.user).order_by('-id')
    obj = []
    for item in items:
        container = ['lost', item]
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Personal Found List
@login_required
def MyFoundListView(request):
    context = {
        'ojects': None,
        'myFoundList': True,
    }
    items = ItemFound.objects.filter(user=request.user).order_by('-id')
    obj = []
    for item in items:
        container = ['found', item]
        obj.append(container)
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Personal Claim List
@login_required
def MyClaimListView(request):
    context = {
        'ojects': None,
        'myClaimList': True,
    }
    items1 = ItemClaim.objects.filter(user=request.user).order_by('-id')
    obj = []
    for item1 in items1:
        item2 = ItemFound.objects.get(id=item1.item.id)
        obj.append(["claim", item1, item2])
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Personal Return List
@login_required
def MyReturnListView(request):
    context = {
        'ojects': None,
        'myReturnList': True,
    }
    items1 = ItemReturn.objects.filter(user=request.user).order_by('-id')
    obj = []
    for item1 in items1:
        item2 = ItemLost.objects.get(id=item1.item.id)
        obj.append(["return", item1, item2])
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Submit Lost
@login_required
def SubmitLostView(request):
    context = {
        'lostForm': True,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        user = request.user
        
        item = ItemLost.objects.create(name=name, place=place, date=datetime.datetime.strptime(date, "%Y-%m-%d").date(), time=datetime.datetime.strptime(time, "%H:%M").time(), description=description, category=category, user=user)
        if image:
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{user.id}/item_lost_images')
            image_file = fileStorage.save(image.name, image)
            item.image = f"{user.id}/item_lost_images/" + str(image_file)
            item.save()
        Post.objects.create(itemLost=item,user=request.user)
        return redirect('/')
    return render(request, template_name="posts/form.html", context=context)

#Submit Found
@login_required
def SubmitFoundView(request):
    context = {
        'foundForm': True,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        user = request.user
        item = ItemFound.objects.create(name=name, place=place, date=datetime.datetime.strptime(date, "%Y-%m-%d").date(), time=datetime.datetime.strptime(time, "%H:%M").time(), description=description, category=category, user=user)
        if image:
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{user.id}/item_found_images')
            image_file = fileStorage.save(image.name, image)
            item.image = f"{user.id}/item_found_images/" + str(image_file)
            item.save()
        Post.objects.create(itemFound=item,user=request.user)
        return redirect('/')
    return render(request, template_name="posts/form.html", context=context)

#Submit Claim
@login_required
def SubmitClaimView(request, itemId):
    context = {
        'claimForm': True,
        'item': ItemFound.objects.get(id=itemId),
    }
    if request.user == context['item'].user:
        return redirect(f"/item/found/{context['item'].id}")
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        user = request.user
        
        item = ItemClaim.objects.create(name=name, place=place, date=datetime.datetime.strptime(date, "%Y-%m-%d").date(), time=datetime.datetime.strptime(time, "%H:%M").time(), description=description, category=context['item'].category, user=user, item=context['item'])
        if image:
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{user.id}/item_claim_images')
            image_file = fileStorage.save(image.name, image)
            item.image = f"{user.id}/item_claim_images/" + str(image_file)
            item.save()
        return redirect('/item/found/'+str(itemId))
    return render(request, template_name="posts/form.html", context=context)

#Submit Return
@login_required
def SubmitReturnView(request, itemId):
    context = {
        'returnForm': True,
        'item': ItemLost.objects.get(id=itemId),
    }
    if request.user == context['item'].user:
        return redirect(f"/item/lost/{context['item'].id}")
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        user = request.user
        
        item = ItemReturn.objects.create(name=name, place=place, date=datetime.datetime.strptime(date, "%Y-%m-%d").date(), time=datetime.datetime.strptime(time, "%H:%M").time(), description=description, category=context['item'].category, user=user, item=context['item'])
        if image:
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{user.id}/item_return_images')
            image_file = fileStorage.save(image.name, image)
            item.image = f"{user.id}/item_return_images/" + str(image_file)
            item.save()
        return redirect('/item/lost/'+str(itemId))
    return render(request, template_name="posts/form.html", context=context)

#Item
def ItemView(request, option, itemId):
    if option == 'lost':
        context = {
            'item': ItemLost.objects.get(id=itemId),
            'option': option,
        }
        return render(request, template_name="posts/item.html", context=context)
    if option == 'found':
        context = {
            'item': ItemFound.objects.get(id=itemId),
            'option': option,
        }
        return render(request, template_name="posts/item.html", context=context)
    if option == 'claim':
        context = {
            'item': ItemClaim.objects.get(id=itemId),
            'option': option,
        }
        return render(request, template_name="posts/item.html", context=context)
    if option == 'return':
        context = {
            'item': ItemReturn.objects.get(id=itemId),
            'option': option,
        }
        return render(request, template_name="posts/item.html", context=context)

#Edit
@login_required
def EditView(request, option, itemId):
    if option == 'lost':
        context = {
            'item': ItemLost.objects.get(id=itemId),
            'option': option,
            'date': None,
            'time': None,
        }
        context['date'] = context['item'].date.strftime('%Y-%m-%d')
        context['time'] = context['item'].time.strftime('%H:%M')
    if option == 'found':
        context = {
            'item': ItemFound.objects.get(id=itemId),
            'option': option,
            'date': None,
            'time': None,
        }
        context['date'] = context['item'].date.strftime('%Y-%m-%d')
        context['time'] = context['item'].time.strftime('%H:%M')
    if option == 'claim':
        context = {
            'item': ItemClaim.objects.get(id=itemId),
            'option': option,
            'date': None,
            'time': None,
        }
        context['date'] = context['item'].date.strftime('%Y-%m-%d')
        context['time'] = context['item'].time.strftime('%H:%M')
    if option == 'return':
        context = {
            'item': ItemReturn.objects.get(id=itemId),
            'option': option,
            'date': None,
            'time': None,
        }
        context['date'] = context['item'].date.strftime('%Y-%m-%d')
        context['time'] = context['item'].time.strftime('%H:%M')
    if request.method == 'POST' and request.user == context['item'].user:
        context['item'].name = request.POST.get('name')
        context['item'].place = request.POST.get('place')
        context['item'].date = datetime.datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()
        context['item'].time = time=datetime.datetime.strptime(request.POST.get('time'), "%H:%M").time()
        context['item'].description = request.POST.get('description')
        if option == 'lost' or option == 'found':
            context['item'].category = request.POST.get('category')
        image = request.FILES.get('image')
        if image:
            if option == 'lost':
                fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_lost_images')
                prev_image = context['item'].image
                if not prev_image == 'default/item_lost_images/default.jpg':
                    fileStorage.delete(str(prev_image).split(f'{request.user.id}/item_lost_images/', 1)[1]) #Instead f'{request.user.id}/item_lost_images/', we can also use 's/'
                image_file = fileStorage.save(image.name, image)
                context['item'].image = f"{request.user.id}/item_lost_images/" + str(image_file)
            if option == 'found':
                fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_found_images')
                prev_image = context['item'].image
                if not prev_image == 'default/item_found_images/default.jpg':
                    fileStorage.delete(str(prev_image).split(f'{request.user.id}/item_found_images/', 1)[1]) #Instead f'{request.user.id}/item_found_images/', we can also use 's/'
                image_file = fileStorage.save(image.name, image)
                context['item'].image = f"{request.user.id}/item_found_images/" + str(image_file)
            if option == 'claim':
                fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_claim_images')
                prev_image = context['item'].image
                if not prev_image == 'default/item_claim_images/default.jpg':
                    fileStorage.delete(str(prev_image).split(f'{request.user.id}/item_claim_images/', 1)[1]) #Instead f'{request.user.id}/item_claim_images/', we can also use 's/'
                image_file = fileStorage.save(image.name, image)
                context['item'].image = f"{request.user.id}/item_claim_images/" + str(image_file)
            if option == 'return':
                fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_return_images')
                prev_image = context['item'].image
                if not prev_image == 'default/item_return_images/default.jpg':
                    fileStorage.delete(str(prev_image).split(f'{request.user.id}/item_return_images/', 1)[1]) #Instead f'{request.user.id}/item_return_images/', we can also use 's/'
                image_file = fileStorage.save(image.name, image)
                context['item'].image = f"{request.user.id}/item_return_images/" + str(image_file)
        context['item'].save()
        if option == 'lost':
            return redirect(f'/item/lost/{itemId}')
        if option == 'found':
            return redirect(f'/item/found/{itemId}')
        if option == 'claim':
            return redirect(f'/item/claim/{itemId}')
        if option == 'return':
            return redirect(f'/item/return/{itemId}')
    if request.user == context['item'].user:
        return render(request, template_name="posts/form.html", context=context)

#Delete
@login_required
def DeleteView(request, option, itemId):
    if option == 'lost':
        context = {
            'item': ItemLost.objects.get(id=itemId),
            'option': option,
        }
    if option == 'found':
        context = {
            'item': ItemFound.objects.get(id=itemId),
            'option': option,
        }
    if option == 'claim':
        context = {
            'item': ItemClaim.objects.get(id=itemId),
            'option': option,
        } 
    if option == 'return':
        context = {
            'item': ItemReturn.objects.get(id=itemId),
            'option': option,
        }
    if request.user == context['item'].user:
        image = context['item'].image
        if option == 'lost':
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f"{request.user.id}/item_lost_images")
            if not image == 'default/item_lost_images/default.jpg':
                fileStorage.delete(str(image).split(f'{request.user.id}/item_lost_images/', 1)[1]) #Instead f'{request.user.id}/item_lost_images/', we can also use 's/'
        if option == 'found':
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_found_images')
            if not image == 'default/item_found_images/default.jpg':
                fileStorage.delete(str(image).split(f'{request.user.id}/item_found_images/', 1)[1]) #Instead f'{request.user.id}/item_found_images/', we can also use 's/'
        if option == 'claim':
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_claim_images')
            if not image == 'default/item_claim_images/default.jpg':
                fileStorage.delete(str(image).split(f'{request.user.id}/item_claim_images/', 1)[1]) #Instead f'{request.user.id}/item_claim_images/', we can also use 's/'
        if option == 'return':
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/item_return_images')
            if not image == 'default/item_return_images/default.jpg':
                fileStorage.delete(str(image).split(f'{request.user.id}/item_return_images/', 1)[1]) #Instead f'{request.user.id}/item_return_images/', we can also use 's/'
        context['item'].delete()
    return redirect('/')

#Claim List
def ClaimListView(request):
    context = {
        'objects': None,
        'claimList': True,
    }
    items1 = ItemFound.objects.filter(user=request.user)
    obj = []
    for item1 in items1:
        items2 = ItemClaim.objects.filter(item=item1)
        for item2 in items2:
            obj.append(["claim", item2])
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)

#Return List
def ReturnListView(request):
    context = {
        'objects': None,
        'returnList': True,
    }
    items1 = ItemLost.objects.filter(user=request.user)
    obj = []
    for item1 in items1:
        items2 = ItemReturn.objects.filter(item=item1)
        for item2 in items2:
            obj.append(["return", item2])
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    context['objects'] = paginator.get_page(page)
    return render(request, template_name="posts/list.html", context=context)