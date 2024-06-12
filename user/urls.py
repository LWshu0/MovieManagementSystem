from django.urls import path

from . import views

urlpatterns = [
    path("login", views.user_login, name="login"),
    path("signup", views.user_signup, name="signup"),
    path("home", views.user_home, name="home"),
    path("myspace", views.user_myspace, name="myspace"),
]