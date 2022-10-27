from django.urls import path
from django.contrib import admin
from . import views
from .views import (
    HomeView,
    Login,
    OurStory,
    RegisterView,
    Logout,
    ArticleCreateView,
    EditArticle,
    )

urlpatterns = [
    # path('', views.home, name='home'),
    # path("login", views.login_view, name="login_view"),
    # path("logout_view", views.logout_view, name="logout_view"),
    # path("register", views.register, name="register"),
    path("create_article", ArticleCreateView.as_view(template_name = "web/create_article.html"), name="create_article"),
    path("tag/<slug:slug>/", views.tagged, name="tagged"),
    path("edit/<int:pk>/", EditArticle.as_view(template_name = "web/update_article.html"), name="edit_article"),
    path('article_detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('like/<int:pk>', views.like, name='like'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('delete', views.delete, name='delete'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_user_info, name='edit_user_info'),
    path('create_user_info', views.create_user_info, name='create_user_info'),
    path('about', OurStory.as_view(), name='our_story'),
    path('written', views.written_stories, name='written_stories'),
    path('',
        HomeView.as_view(template_name='web/home.html'),
        name='home',
        ),
    path('register',
        RegisterView.as_view(template_name='web/class_register.html'),
        name='class_register_view',
        ),
    path('login',
        Login.as_view(template_name='web/class_login.html'),
        name='class_login_view',
        ),
    path('logout',
        Logout.as_view(),
        name='class_logout',
        ),




]
