from django.shortcuts import render , redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import UserProfile
from .forms import SignUpForm, SignInForm
from posts.models import Post, PostLike, PostBookmark, PostComment




# Create your views here.



def sign_in(request: HttpRequest):

    if request.method == "POST":
        form = SignInForm(request.POST)

        # check form fields
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # check auth
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully", "alert-success")
                return redirect(request.GET.get("next", "/"))
            else:
                messages.error(request, "Invalid username or password.", "alert-danger")

        else:
            # form errors
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = SignInForm()

    return render(request, "accounts/signin.html", {"form": form})

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
                print(e)
                messages.error(request, "Something went wrong, try again.", "alert-danger")

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
        return redirect("main:home")   




    recent_posts = Post.objects.filter(author=profile_user).order_by("-created_at")[:3]

    liked_posts = Post.objects.filter(likes__user=profile_user).distinct()[:3]

    bookmarked_posts = Post.objects.filter(bookmarks_post__user=profile_user).distinct()[:3]

    commented_posts = Post.objects.filter(comments__user=profile_user).distinct()[:3]



    return render(request, 'accounts/profile.html', {
        "profile_user": profile_user,

        "recent_posts": recent_posts,
        "liked_posts": liked_posts,
        "bookmarked_posts": bookmarked_posts,
        "commented_posts": commented_posts,
    })


def log_out(request: HttpRequest):
    logout(request) 
    messages.success(request, "Logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/")) 




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
            print(e)

    return render(request, "accounts/update_profile.html")

def user_posts_view(request, user_name):

    try:
        profile_user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return redirect("main:home")

    posts = Post.objects.filter(author=profile_user).order_by("-created_at")

    return render(request, "accounts/user_posts.html", {
        "profile_user": profile_user,
        "posts": posts,
        "page_title": "All Posts",
    })



def user_liked_posts_view(request, user_name):

    try:
        profile_user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return redirect("main:home")

    posts = Post.objects.filter(likes__user=profile_user).distinct()

    return render(request, "accounts/user_posts.html", {
        "profile_user": profile_user,
        "posts": posts,
        "page_title": "Liked Posts",
    })



def user_bookmarked_posts_view(request, user_name):

    try:
        profile_user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return redirect("main:home")

    posts = Post.objects.filter(bookmarks_post__user=profile_user).distinct()

    return render(request, "accounts/user_posts.html", {
        "profile_user": profile_user,
        "posts": posts,
        "page_title": "Bookmarked Posts",
    })



def user_commented_posts_view(request, user_name):

    try:
        profile_user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return redirect("main:home")

    posts = Post.objects.filter(comments__user=profile_user).distinct()

    return render(request, "accounts/user_posts.html", {
        "profile_user": profile_user,
        "posts": posts,
        "page_title": "Commented Posts",
    })

