from django.urls import path

from . import views

app_name = 'manager'

urlpatterns = [
    path("test", views.test, name="test"),
    #director
    path('director/', views.manager_director),
    path('director_add/', views.manager_director_add),
    path('director_delete/', views.manager_director_delete),
    path('director_update/', views.manager_director_update),
    #movie
    path('movie/', views.manager_movie),
    path('movie_add/', views.manager_movie_add),
    path('movie_delete/',views.manager_movie_delete),
    path('movie_update/', views.manager_movie_update),
    # user
    path('user/', views.manager_user),
    path('user_add/', views.manager_user_add),
    path('user_delete/', views.manager_user_delete),
    path('user_update/', views.manager_user_update),
    # review
    path('review/', views.manager_review),
    path('review_add/', views.manager_review_add),
    path('review_delete/', views.manager_review_delete),
    path('review_update/', views.manager_review_update),
    # like
    path('like/', views.manager_like),
    path('like_add/', views.manager_like_add),
    path('like_delete/', views.manager_like_delete),
    # actor
    path('actor/', views.manager_actor),
    path('actor_add/', views.manager_actor_add),
    path('actor_delete/', views.manager_actor_delete),
    path('actor_update/', views.manager_actor_update),
    # cast
    path('cast/', views.manager_cast),
    path('cast_add/', views.manager_cast_add),
    path('cast_delete/', views.manager_cast_delete),
]
