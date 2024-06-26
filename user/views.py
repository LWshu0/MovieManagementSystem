from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import hashlib
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse

# model
from .models import User, Movie, Like, Review, Cast

# Create your views here.
def initial(request):
    return redirect("/user/login")

#用户界面-----------------------------------------------------------------------------
@csrf_protect
def user_login(request):
    method = request.method
    if method == "GET":
        print('user login get')
        return render(request, "user/login.html")
    elif method == "POST":
        print('user login post')
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            user_id = user.id
            res = password + settings.SECRET_KEY
            password = hashlib.md5(res.encode("utf-8")).hexdigest()
            if password == user.password:
                if user.username == "manager":
                    return redirect("/manager/director")
                else:
                    return redirect(reverse('user_home', args=[user_id]))
            else:
                return render(request, "user/login.html", {"tip": "密码错误！"})
        except User.DoesNotExist:
            return render(request, "user/login.html", {"tip": "用户名不存在！"})
        
@csrf_protect
def user_signup(request):
    if request.method == "GET":
        return render(request, "user/signup.html")
    elif request.method == "POST":
        get_post = request.POST
        username = get_post.get("username")
        print('username:', username)
        password = get_post.get("password")
        print('password:', password)
        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()
        gender = get_post.get("gender")
        if User.objects.filter(username=username).exists():
            return render(request, "user/signup.html", {"msg": "注册失败，用户名已存在!"})
        else:
            User.objects.create(username=username, password=password, gender=gender)
            return redirect("/user/login", {"tip2": "注册成功！"})

@csrf_protect
def user_home(request, userID):
    if request.method == "GET":
        movies = Movie.objects.all()
        user = User.objects.get(id=userID)
        return render(request, 'user/home.html', {'user': user, 'movies': movies})
    if request.method == "POST":
        search_query = request.POST.get('search')
        user = User.objects.get(id=userID)
        movies = Movie.objects.filter(
            Q(moviename__icontains=search_query) |  # 电影名称模糊搜索
            Q(director__directorname__icontains=search_query) |  # 导演名称模糊搜索
            Q(type__icontains=search_query) |  # 类型模糊搜索
            Q(time__icontains=search_query) |  # 时间模糊搜索
            Q(area__icontains=search_query))  # 地区模糊搜索
        return render(request, 'user/home.html', {'movies': movies, "user": user, "search_query": search_query})
    
def user_myspace(request, userID):
    user = User.objects.get(id=userID)
    # 获取用户喜欢的电影
    likes = Like.objects.filter(user=user)
    liked_movies = [like.movie for like in likes]
    # 获取用户的评论
    reviews = Review.objects.filter(user=user)
    context = {
        'user': user,
        'movies': liked_movies,
        'reviews': reviews,
    }
    return render(request, 'user/myspace.html', context)

def user_movie(request, userID, movieID):
    if request.method == "GET":
        user = User.objects.get(id=userID)
        movie = Movie.objects.get(id=movieID)
        director = movie.director
        reviews = Review.objects.filter(movie=movie)
        cast_list = Cast.objects.filter(movie=movie)
        actors = [cast.actor for cast in cast_list]

        context = {
            'movie': movie,
            'director': director,
            'user': user,
            'reviews': reviews,
            'actors': actors
        }
        return render(request, 'user/movie.html', context)
    

def add_to_favorites(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        movie = request.POST.get('movie')
        user = request.POST.get('user')
        movie = Movie.objects.get(id=movie)
        user = User.objects.get(id=user)
        Like.objects.create(user=user, movie=movie)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def add_comment(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating')
        movie = Movie.objects.get(id=movie_id)
        user = User.objects.get(id=user_id)
        Review.objects.create(user=user, movie=movie, comment=comment_text, rating=rating)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': '无效的请求'}, status=400)