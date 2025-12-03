from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='log_out'),
    path('update/profile/', views.update_user_profile, name='update_profile'),
    path('profile/<user_name>/', views.user_profile_view, name='user_profile_view'),
    path("<str:user_name>/posts/", views.user_posts_view, name="user_posts"),
    path("<str:user_name>/liked/", views.user_liked_posts_view, name="user_liked_posts"),
    path("<str:user_name>/bookmarks/", views.user_bookmarked_posts_view, name="user_bookmarked_posts"),
    path("<str:user_name>/comments/", views.user_commented_posts_view, name="user_commented_posts"),


]

