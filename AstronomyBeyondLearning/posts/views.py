from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Post, PostLike, PostComment, PostBookmark
from django.views import View
from django.contrib.auth.decorators import login_required        
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import User 
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin



#هنا اللايك 
def like_post(request, post_id):
  
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method. Must be POST.")

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    try:
        like = PostLike.objects.get(user=user, post=post)
        like.delete()
        is_liked = False
        message = "Post unliked successfully."
        
    except PostLike.DoesNotExist:
        PostLike.objects.create(user=user, post=post)
        is_liked = True
        message = "Post liked successfully."

    return JsonResponse({
        'is_liked': is_liked,
        'total_likes': post.total_likes,
        'message': message
    })
    
    
    #انشاء بوست
def create_post_view(request):
    # التأكد من أن المستخدم هو المسؤول
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to create a post.")
        return redirect("accounts:login")  # التوجيه إلى صفحة الدخول إذا لم يكن المستخدم مسجل دخول

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        media_file = request.FILES.get("media_file")  # رفع صورة أو فيديو
        
        # التحقق من البيانات
        if not title or not content:
            messages.warning(request, "Title and content are required.")
            return redirect("posts:create_post")

        # إنشاء المنشور
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

    #تعديل البوست
def edit_post(request, post_id):

    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method. Must be POST.")

    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_staff_or_above = user.role in ['Staff', 'Moderator', 'Admin']
    
    if post.author == user or is_staff_or_above:
        import json
        try:
            data = json.loads(request.body)

            post.title = data.get('title', post.title)
            post.content = data.get('body', post.content)
            post.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Post updated successfully.',
                'title': post.title,
                'content': post.content
            }, status=200)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
    
    return HttpResponseForbidden("You do not have permission to edit this post.")
    
    
      # حذف بوست
def delete_post(request, post_id): 
    
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method. Must be POST.")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found.")

    user = request.user
    is_staff_or_above = user.role in ['Staff', 'Moderator', 'Admin']
    
    if post.author == user or is_staff_or_above:
        post.delete() 
        return JsonResponse({'success': True, 'message': 'Post deleted successfully.'}, status=200)

    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")
    
    
    #تفاصيل البوست
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
   
   
    #جميع البوستات
def all_posts_view(request):
        posts = Post.objects.all().order_by('-created_at')
    
        context = {
        'posts': posts
    }
        return render(request, 'posts/all_posts.html', context)

    #هنا اضافة كومنت 
def add_comment(request, post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        import json
        try:
            data = json.loads(request.body)
            comment_body = data.get('body', '').strip()
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")

        if not comment_body:
            return JsonResponse({'error': 'Comment body cannot be empty.'}, status=400)

        new_comment = PostComment.objects.create(
            user=request.user,
            post=post,
            body=comment_body
        )
        
        return JsonResponse({
            'success': True,
            'id': new_comment.id,
            'body': new_comment.body,
            'username': request.user.username,
            'created_at': new_comment.created_at.strftime("%b %d, %Y %H:%M") 
        }, status=201) 
        
    return HttpResponseBadRequest("Invalid request method.")


      # هنا حذف الكومنت 
def delete_comment(request, comment_id):
    
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    try:
        comment = PostComment.objects.get(id=comment_id)
    except PostComment.DoesNotExist:
        raise Http404("Comment not found.")

    user = request.user
    is_moderator_or_staff = user.role in ['Moderator', 'Staff', 'Admin']
    
    if comment.user == user or is_moderator_or_staff:
        comment.delete() 
        return JsonResponse({'success': True, 'message': 'Comment deleted.'}, status=200)

    else:
        return HttpResponseForbidden("You do not have permission to delete this comment.")
    
    
    #هنا الحفظ 
def post_bookmark(request, post_id):
   
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method. Must be POST.")

    post = get_object_or_404(Post, id=post_id)
    user = request.user 

    try:
        bookmark = PostBookmark.objects.get(user=user, post=post)
        bookmark.delete()
        is_bookmarked = False
        message = "Post unsaved successfully."
        
    except PostBookmark.DoesNotExist:
        PostBookmark.objects.create(user=user, post=post)
        is_bookmarked = True
        message = "Post saved successfully."

    return JsonResponse({
        'is_bookmarked': is_bookmarked,
        'message': message
    })
    
   