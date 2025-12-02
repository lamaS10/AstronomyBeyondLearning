from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User

 
    #مودل البوست 
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text='The user who created the post.'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    media_file = models.FileField(
        upload_to='post_media/', 
        blank=True, 
        null=True,
        help_text='Image or video file for the post.'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] 
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
        
        #مودل اللايك
class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text='The user who performed the like action.'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text='The post that was liked.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') 
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'
    
   
   
    #مودل الكومنت 
class PostComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The user who wrote the comment.'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The post the comment belongs to.'
    )
    body = models.TextField(help_text='The text content of the comment.')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(
        default=False, 
        help_text='Marks the comment as deleted by a moderator.'
    ) 

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title[:20]}'

    class Meta:
        ordering = ['created_at'] 
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        
       
       
        #مودل البوك مارك
class PostBookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookmarks_post',
        help_text='The user who bookmarked the post.'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='bookmarks_post',
        help_text='The post that was bookmarked.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') 
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f'{self.user.username} bookmarked {self.post.title}'