from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, models
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
from django.core.files.storage import FileSystemStorage
from app.settings import MEDIA_ROOT

# Create your views here.
#Login and Registration
def RegisterLoginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {
        'successFlag': False,
        'usernameErrorFlag': False,
        'passwordErrorFlag': False,
        'errorFlag': False,
        'signup': False,
        'username': "",
        'email': "",
        'fname': "",
        "lname": ""
    }
    if request.method == "POST":
        if 'submit-register' in request.POST:
            context['signup'] = True
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)
            fname = request.POST.get('fname', None)
            lname = request.POST.get('lname', None)
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if username != "" and password1 == password2 and not models.User.objects.filter(username=username).exists():
                context['successFlag'] = True
                context['errorFlag'] = False
                context['signup'] = False
                user = models.User.objects.create_user(username=username, email=email, password=password1, first_name=fname, last_name=lname)
                Profile.objects.create(user=user)
                return redirect('/entry')
            else:
                context['successFlag'] = False
                context['errorFlag'] = True
                context['email'] = email
                context['fname'] = fname
                context['lname'] = lname
                if password1 != password2:
                    context['passwordErrorFlag'] = True
                    context['username'] = username
                if models.User.objects.filter(username=username).exists():
                    context['usernameErrorFlag'] = True
                    context['username'] = ""
        elif 'submit-login' in request.POST:
            context['signup'] = False
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user:
                context['successFlag'] = True
                context['errorFlag'] = False
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('/')
            else:
                context['successFlag'] = False
                context['errorFlag'] = True
    return render(request, template_name="users/register_login.html", context=context)

#Logout
def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

#Profile
@login_required
def ProfileView(request):
    context = {
        'objects': None,
    }
    posts = Post.objects.filter(user=request.user).order_by('-id')[:4]
    obj = []
    for post in posts:
        container = []
        if post.itemLost:
            container.extend(["lost",post.itemLost])
        if post.itemFound:
            container.extend(["found",post.itemFound])
        obj.append(container)
    context['objects'] = obj
    return render(request, template_name="users/profile.html", context=context)

#Update Profile
@login_required
def UpdateProfileView(request):
    context = {}
    if request.method == 'POST':
        print(request.user)
        user = request.user
        profile = Profile.objects.get(user=user)
        image = request.FILES.get('image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        if image:
            fileStorage = FileSystemStorage(location=MEDIA_ROOT/f'{request.user.id}/profile_pics')
            image_file = fileStorage.save(image.name, image)
            profile.image = f'{request.user.id}/profile_pics/' + str(image_file)
            profile.save()
        return redirect('/profile')
    return render(request, template_name='users/update.html', context=context)