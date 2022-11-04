from django.urls import path

from django.contrib import admin
from . import views
from .views import (
    ArticleDetail,
    HomeView,
    Login,
    OurStory,
    ProfileView,
    RegisterView,
    Logout,
    ArticleCreateView,
    EditArticle,
    #EditUserView,
    Tagged,
    WrittenStories,
    DeleteView,
    ArticleDetail,
    ProfileCreateView,
    )
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        '',
        HomeView.as_view(template_name='web/home.html'),
        name='home',
        ),
    path(
        "create_article",
        login_required(
            ArticleCreateView.as_view(template_name = "web/create_article.html")
            ),
        name="create_article"
        ),
    path(
        "tag/<slug:slug>/",
        Tagged.as_view(template_name = "web/home.html" ),
        name="tagged"
        ),
    path(
        "edit/<int:pk>/",
        login_required(
            EditArticle.as_view(template_name = "web/update_article.html")
            ),
         name="edit_article"
         ),
    path(
        'article_detail/<int:pk>/',
        login_required(
            ArticleDetail.as_view(template_name = "web/article_detail_view.html")
        ),
        name='article_detail'
        ),
    path('like/<int:pk>', views.like, name='like'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path(
        'delete/<int:pk>/',
        login_required(DeleteView.as_view()),
            name='delete'
            ),
    path('profile',
        login_required(ProfileView.as_view()),
        name='profile'
        ),
    #path('edit_profile', EditUserView.as_view(template_name = "web/update_user_info.html"), name='edit_user_info'),
    path('edit_profile', views.edit_user_info, name='edit_user_info'),
    path(
        'create_user_info',
        login_required(ProfileCreateView.as_view(
            template_name = "web/create_user_info.html"
            )),
        name='create_user_info'
        ),
    path('about', OurStory.as_view(), name='our_story'),
    path(
        'written',
        login_required(
            WrittenStories.as_view(template_name = "web/written_stories.html")
            ),
        name='written_stories'
        ),

    path(
        'register',
        RegisterView.as_view(template_name='web/register.html'),
        name='register',
        ),
    path(
        'login',
        Login.as_view(template_name='web/login.html'),
        name='login_view',
        ),
    path(
        'logout',
        Logout.as_view(),
        name='logout',
        ),




]
