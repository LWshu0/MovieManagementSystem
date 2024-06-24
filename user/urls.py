from django.urls import path

from . import views

urlpatterns = [
    path("user/login", views.user_login, name="login"),
    path("user/signup", views.user_signup, name="signup"),
    path("<str:userID>/home", views.user_home, name="user_home"),
    path("<str:userID>/myspace", views.user_myspace, name="user_myspace"),
    path("<str:userID>/<str:movieID>", views.user_movie, name="user_movie"),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('add_comment/', views.add_comment, name='add_comment'),
]