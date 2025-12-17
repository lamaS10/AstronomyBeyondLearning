from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, Http404
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from .models import Post, PostLike, PostComment, PostBookmark


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

    return HttpResponseBadRequest("Invalid request method.")


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

        new_post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            media_file=media_file
        )
        messages.success(request, "Post created successfully!")
        return redirect('posts:post_detail', post_id=new_post.id)

    return render(request, "posts/create_post.html")


# Edit post
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-styled'}),
            'content': forms.Textarea(attrs={'class': 'form-input-styled'}),
            'media_file': forms.FileInput(),
        }


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
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        is_author = (post.author == user)
        is_super_or_staff = (user.is_superuser or user.is_staff)
        is_moderator = user.groups.filter(name="moderator").exists()

        if is_author or is_super_or_staff or is_moderator:
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('posts:all_posts')

        messages.error(request, "You do not have permission to delete this post.")
        return redirect('posts:post_detail', post_id=post.id)

    return HttpResponseBadRequest("Invalid request method.")


# Post detail
def post_detail_view(request, post_id):

    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
    comments = PostComment.objects.filter(post=post).order_by('created_at')

    is_liked = is_bookmarked = False

    if request.user.is_authenticated:
        is_liked = PostLike.objects.filter(post=post, user=request.user).exists()
        is_bookmarked = PostBookmark.objects.filter(post=post, user=request.user).exists()

    is_moderator = False
    if request.user.is_authenticated:
        is_moderator = request.user.groups.filter(name="moderator").exists()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
        'is_moderator': is_moderator,
    }

    return render(request, 'posts/post_detail.html', context)


# All posts
def all_posts_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/all_posts.html', {'posts': posts})


# Add comment
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add a comment.")
        return redirect('accounts:sign_in')

    if request.method == 'POST':
        body = request.POST.get('comment_body')

        if body:
            PostComment.objects.create(post=post, user=request.user, body=body)
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Cannot add an empty comment.")

        return redirect('posts:post_detail', post_id=post.id)

    return redirect('posts:post_detail', post_id=post.id)


# Delete comment
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, id=comment_id)
        user = request.user

        has_perm = (comment.user == user or user.has_perm("posts.delete_postcomment"))

        if has_perm:
            post_id = comment.post.id
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
            return redirect('posts:post_detail', post_id=post_id)

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
            messages.info(request, "Bookmark removed.")
        except PostBookmark.DoesNotExist:
            PostBookmark.objects.create(user=user, post=post)
            messages.success(request, "Post bookmarked.")

        return redirect('posts:post_detail', post_id=post.id)

    return HttpResponseBadRequest("Invalid request method.")


# Search
def post_search_view(request):
    query = request.GET.get("search")
    posts = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'posts/search_posts.html', {'posts': posts, 'query': query})
