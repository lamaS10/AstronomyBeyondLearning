from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Post, PostLike, PostComment, PostBookmark, PostComment
from django.views import View
from django import forms
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import User 
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


# Like post
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        try:
            like = PostLike.objects.get(user=user, post=post)
            like.delete()
            messages.info(request, "Post unliked successfully.")
            
        except PostLike.DoesNotExist:
            PostLike.objects.create(user=user, post=post)
            messages.success(request, "Post liked successfully!")

        return redirect('posts:post_detail', post_id=post.id)
        
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
    
    # Create post
def create_post_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to create a post.")
        return redirect("accounts:sign_in")  

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        media_file = request.FILES.get("media_file")  
        
        if not title or not content:
            messages.warning(request, "Title and content are required.")
            return redirect("posts:create_post")

        try:
            new_post = Post.objects.create(
                author=request.user,
                title=title,
                content=content,
                media_file=media_file
            )
            messages.success(request, "Post created successfully!")
            return redirect('posts:post_detail', post_id=new_post.id)

        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")
            return redirect("posts:create_post")

    return render(request, "posts/create_post.html")


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-styled'}),
            'content': forms.Textarea(attrs={'class': 'form-input-styled'}),
            'media_file': forms.FileInput(), 
        }

# Edit post
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if post.author != user and not user.is_superuser and not user.is_staff:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('posts:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            form.save() 
            messages.success(request, "Post edited successfully.")
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostEditForm(instance=post)
        
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})
    
    # Delete post
def delete_post(request, post_id): 
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, "Sorry, the requested post was not found.")
            return redirect('posts:all_posts') 

        user = request.user
        is_staff_or_above = user.is_superuser or user.is_staff 
        
        if post.author == user or is_staff_or_above:
            post.delete() 
            messages.success(request, "Post deleted successfully.")
            return redirect('posts:all_posts') 

        else:
            messages.error(request, "You do not have permission to delete this post.")
            return redirect('posts:post_detail', post_id=post.id)
            
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
    
    
    # Post details
def post_detail_view(request, post_id):
   
    post = get_object_or_404(
        Post.objects.select_related('author'), 
        id=post_id
    )
    
    comments = PostComment.objects.filter(post=post).order_by('created_at')
    
    is_liked = False
    is_bookmarked = False
    if request.user.is_authenticated:
        is_liked = PostLike.objects.filter(post=post, user=request.user).exists()
        is_bookmarked = PostBookmark.objects.filter(post=post, user=request.user).exists()
        
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
    }
    
    return render(request, 'posts/post_detail.html', context)
   
   
    # All posts
def all_posts_view(request):
        posts = Post.objects.all().order_by('-created_at')
        context = {
        'posts': posts
    }
  
        return render(request, 'posts/all_posts.html', context)

    # Add comment
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add a comment.")
        return redirect('accounts:login') 
        
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body') 
        
        if comment_body:
            PostComment.objects.create(
                post=post,
                user=request.user,
                body=comment_body 
            )
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Cannot add an empty comment.")

        return redirect('posts:post_detail', post_id=post.id) 
        
    return redirect('posts:post_detail', post_id=post.id)


      # Delete comment 
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = PostComment.objects.get(id=comment_id)
        except PostComment.DoesNotExist:
            messages.error(request, "Comment not found.")
            raise Http404("Comment not found.")

        user = request.user
        is_moderator_or_staff = user.role in ['Moderator', 'Staff', 'Admin']
        
        if comment.user == user or is_moderator_or_staff:
            post_id = comment.post.id 
            comment.delete() 
            messages.success(request, 'Comment deleted successfully.')
            return redirect('posts:post_detail', post_id=post_id)

        else:
            messages.error(request, "You do not have permission to delete this comment.")
            return redirect('posts:post_detail', post_id=comment.post.id)
            
    return HttpResponseBadRequest("Invalid request method.")
    
    
    # Bookmark post
def post_bookmark(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user 

        try:
            bookmark = PostBookmark.objects.get(user=user, post=post)
            bookmark.delete()
            messages.info(request, "Bookmark removed from post.")
            
        except PostBookmark.DoesNotExist:
            PostBookmark.objects.create(user=user, post=post)
            messages.success(request, "Post bookmarked successfully.")

        return redirect('posts:post_detail', post_id=post.id)
        
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
