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
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        try:
            like = PostLike.objects.get(user=user, post=post)
            like.delete()
            messages.info(request, "تم إلغاء الإعجاب بالمنشور بنجاح.")
            
        except PostLike.DoesNotExist:
            PostLike.objects.create(user=user, post=post)
            messages.success(request, "تم الإعجاب بالمنشور بنجاح!")

        return redirect('posts:post_detail', post_id=post.id)
        
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
    
    #انشاء بوست
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


    #تعديل البوست
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_staff_or_above = user.role in ['Staff', 'Moderator', 'Admin']
    
    if not (post.author == user or is_staff_or_above):
        messages.error(request, "ليس لديك صلاحية لتعديل هذا المنشور.")
        return redirect('posts:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')
        
        if new_title and new_content:
            post.title = new_title
            post.content = new_content
            post.save()
            messages.success(request, "تم تحديث المنشور بنجاح.")
            return redirect('posts:post_detail', post_id=post.id)
        else:
            messages.warning(request, "العنوان والمحتوى لا يمكن أن يكونا فارغين.")
            return redirect('posts:edit_post_template', post_id=post.id) 
        
            return render(request, 'posts/edit_post.html', {'post': post})
    
    
      # حذف بوست
def delete_post(request, post_id): 
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, "لم يتم العثور على المنشور.")
            raise Http404("Post not found.")

        user = request.user
        is_staff_or_above = user.role in ['Staff', 'Moderator', 'Admin']
        
        if post.author == user or is_staff_or_above:
            post.delete() 
            messages.success(request, "تم حذف المنشور بنجاح.")
            return redirect('posts:all_posts') 

        else:
            messages.error(request, "ليس لديك صلاحية لحذف هذا المنشور.")
            return redirect('posts:post_detail', post_id=post.id)
            
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
    
    
    
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
        comment_body = request.POST.get('comment_body', '').strip()

        if not comment_body:
            messages.warning(request, 'لا يمكن ترك التعليق فارغًا.')
            return redirect('posts:post_detail', post_id=post.id)

        PostComment.objects.create(
            user=request.user,
            post=post,
            body=comment_body
        )
        
        messages.success(request, 'تم إضافة التعليق بنجاح.')
        return redirect(f'/posts/{post.id}#comments')
        
    return HttpResponseBadRequest("Invalid request method.")


      # هنا حذف الكومنت 
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = PostComment.objects.get(id=comment_id)
        except PostComment.DoesNotExist:
            messages.error(request, "لم يتم العثور على التعليق.")
            raise Http404("Comment not found.")

        user = request.user
        is_moderator_or_staff = user.role in ['Moderator', 'Staff', 'Admin']
        
        if comment.user == user or is_moderator_or_staff:
            post_id = comment.post.id 
            comment.delete() 
            messages.success(request, 'تم حذف التعليق بنجاح.')
            return redirect('posts:post_detail', post_id=post_id)

        else:
            messages.error(request, "ليس لديك صلاحية لحذف هذا التعليق.")
            return redirect('posts:post_detail', post_id=comment.post.id)
            
    return HttpResponseBadRequest("Invalid request method.")
    
    
    
    #هنا الحفظ 
def post_bookmark(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user 

        try:
            bookmark = PostBookmark.objects.get(user=user, post=post)
            bookmark.delete()
            messages.info(request, "تم إلغاء حفظ المنشور.")
            
        except PostBookmark.DoesNotExist:
            PostBookmark.objects.create(user=user, post=post)
            messages.success(request, "تم حفظ المنشور بنجاح.")

        return redirect('posts:post_detail', post_id=post.id)
        
    return HttpResponseBadRequest("Invalid request method. Must be POST.")
    
   