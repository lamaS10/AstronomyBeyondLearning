from django.urls import path 
from . import views

app_name = 'posts'

urlpatterns = [

        path('post/<int:post_id>/like/', views.like_post, name='like_post'),
        path('post/<int:post_id>/comment/add/', views.add_comment, name='add_comment'),
        path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
        path('post/<int:post_id>/bookmark/', views.post_bookmark, name='post_bookmark'),
        path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
        path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
        path('create/', views.create_post_view, name='create_post'),
        path('all/posts', views.all_posts_view, name='all_posts'),
        path('post/<int:post_id>/like/', views.like_post, name='like_post'),
        
                                                                   
]



    
