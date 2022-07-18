"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from home.views import HomeView
from users.views import RegisterLoginView, LogoutView, ProfileView, UpdateProfileView
from posts.views import PostsView, SpecificPostsView, FoundListView, LostListView, SubmitLostView, SubmitFoundView, SubmitClaimView, SubmitReturnView, ItemView, EditView, DeleteView, MyPostsView, MyLostListView, MyFoundListView, MyClaimListView, MyReturnListView, ClaimListView, ReturnListView

urlpatterns = [
    *static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT),
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('lostList/', LostListView, name='globalLostList'),
    path('foundList/', FoundListView, name='globalFoundList'),
    path('entry/', RegisterLoginView, name='register_login'),
    path('logout/', LogoutView, name='logout'),
    path('posts/', PostsView, name="posts"),
    path('posts/<str:option>', SpecificPostsView, name="specificPosts"),
    path('submitLost/', SubmitLostView, name="submitLost"),
    path('submitFound/', SubmitFoundView, name="submitFound"),
    path('submitClaim/<int:itemId>/', SubmitClaimView, name="submitClaim"),
    path('submitReturn/<int:itemId>/', SubmitReturnView, name="submitReturn"),
    path('item/<str:option>/<int:itemId>/', ItemView, name="itemView"),
    path('edit/<str:option>/<int:itemId>/', EditView, name="editView"),
    path('delete/<str:option>/<int:itemId>/', DeleteView, name='deleteView'),
    path('profile/', ProfileView, name='profile'),
    path('profile/update/', UpdateProfileView, name='update'),
    path('profile/posts/', MyPostsView, name='myPosts'),
    path('profile/myLostList/', MyLostListView, name='myLostList'),
    path('profile/myFoundList/', MyFoundListView, name='myFoundList'),
    path('profile/myClaimList/', MyClaimListView, name='myClaimList'),
    path('profile/myReturnList/', MyReturnListView, name='myReturnList'),
    path('profile/claimList/', ClaimListView, name='claimList'),
    path('profile/returnList/', ReturnListView, name='returnList'),
]