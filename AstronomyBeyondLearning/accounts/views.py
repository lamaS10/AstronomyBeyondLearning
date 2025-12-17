from django.shortcuts import render , redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import UserProfile
from .forms import SignUpForm, SignInForm
from posts.models import Post
from django.db.models import Count
from planets.models import BookmarkPlanet
from django.core.paginator import Paginator
from games.models import QuizProgress



def sign_in(request: HttpRequest):

    next_url = request.GET.get("next", "/")  

    if request.method == "POST":
        form = SignInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully", "alert-success")

                next_redirect = request.POST.get("next") or request.GET.get("next") or "/"
                return redirect(next_redirect)

            else:
                messages.error(request, "Invalid username or password.", "alert-danger")

        else:
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = SignInForm()

    return render(request, "accounts/signin.html", {
        "form": form,
        "next": next_url,   
    })


def sign_up(request: HttpRequest):

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)

        # check form
        if form.is_valid():

            # get data
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            bio = form.cleaned_data.get("bio", "")
            website = form.cleaned_data.get("website", "")
            profile_picture = form.cleaned_data.get("profile_picture")

            try:
                with transaction.atomic():

                    # create user
                    new_user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )

                    # create profile
                    UserProfile.objects.create(
                        user=new_user,
                        bio=bio,
                        website=website,
                        profile_picture=profile_picture
                    )

                messages.success(request, "Registered Successfully", "alert-success")
                return redirect("accounts:sign_in")

            except Exception as e:
                messages.error(request, "Something went wrong, try again.", "alert-danger")
                return render(request, "404.html", status=404)

        else:
            # show form errors
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})



def user_profile_view(request: HttpRequest, user_name):

    try:
        profile_user = User.objects.get(username=user_name)

        if not UserProfile.objects.filter(user=profile_user).exists():
            UserProfile.objects.create(user=profile_user)

    except Exception as e:
        print("Profile error:", e)
        return render(request, "404.html", status=404)
    progress = QuizProgress.objects.filter(user=profile_user).first()


    recent_posts = (
        Post.objects.filter(author=profile_user)
        .annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count("comments", distinct=True)
        )
        .order_by("-created_at")[:3]
    )

    show_private_sections = request.user.is_authenticated and request.user == profile_user

    liked_posts = bookmarked_posts = commented_posts = None

    if show_private_sections:
        liked_posts = (
            Post.objects.filter(likes__user=profile_user)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count("comments", distinct=True)
            )
            .distinct()[:3]
        )

        bookmarked_posts = (
            Post.objects.filter(bookmarks_post__user=profile_user)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count("comments", distinct=True)
            )
            .distinct()[:3]
        )

        commented_posts = (
            Post.objects.filter(comments__user=profile_user)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count("comments", distinct=True)
            )
            .distinct()[:3]
        )

    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "recent_posts": recent_posts,
        "liked_posts": liked_posts,
        "bookmarked_posts": bookmarked_posts,
        "commented_posts": commented_posts,
        "show_private_sections": show_private_sections,
        "progress": progress, 
    })


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-warning")

    next_url = request.META.get("HTTP_REFERER", "/")  
    return redirect(next_url)



def update_user_profile(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "alert-warning")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        try:
            with transaction.atomic():

                user: User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile: UserProfile = user.userprofile

                profile.bio = request.POST.get("bio", profile.bio)
                profile.website = request.POST.get("website", profile.website)

                if "profile_picture" in request.FILES:
                    profile.profile_picture = request.FILES["profile_picture"]

                profile.save()

                messages.success(request, "Profile updated successfully!", "alert-success")
                return redirect("accounts:user_profile_view", user_name=user.username)

        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            return render(request, "404.html", status=404)

    return render(request, "accounts/update_profile.html")



def user_posts_type_view(request, user_name, post_type):

    try:
        profile_user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return redirect("main:home")

    posts = Post.objects.all()

    if post_type == "all":
        posts = posts.filter(author=profile_user)

    elif post_type == "liked":
        posts = posts.filter(likes__user=profile_user).distinct()

    elif post_type == "bookmarked":
        posts = posts.filter(bookmarks_post__user=profile_user).distinct()

    elif post_type == "commented":
        posts = posts.filter(comments__user=profile_user).distinct()

    else:
        return redirect("main:home")

    posts = posts.annotate(
        like_count=Count("likes", distinct=True),
        comment_count=Count("comments", distinct=True),
    ).order_by("-created_at")

    paginator = Paginator(posts, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    titles = {
        "all": f"All posts by {profile_user.username}",
        "liked": f"Posts liked by {profile_user.username}",
        "bookmarked": f"Posts bookmarked by {profile_user.username}",
        "commented": f"Posts commented by {profile_user.username}",
    }

    return render(request, "accounts/user_posts.html", {
        "profile_user": profile_user,
        "posts": page_obj, 
        "page_title": titles.get(post_type, "Posts"),
        "paginator": paginator,
    })




def saved_planets_in_profile(request, username):

    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("home")

    if request.user != profile_user:
        messages.error(request, "You are not allowed to view saved planets for this profile.")
        return redirect("accounts:profile", username=request.user.username)

    saved_list = BookmarkPlanet.objects.filter(user=profile_user)

    paginator = Paginator(saved_list, 6)
    page_number = request.GET.get("page")
    saved_planets = paginator.get_page(page_number)

    return render(request, "accounts/saved_planets.html", {
        "profile_user": profile_user,
        "saved_planets": saved_planets, 
    })