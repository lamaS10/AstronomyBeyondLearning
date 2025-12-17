from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy



app_name = 'accounts'

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='log_out'),
    path('update/profile/', views.update_user_profile, name='update_profile'),
    path('<str:user_name>/posts/<str:post_type>/', views.user_posts_type_view, name="user_posts_type"),
    path('profile/<str:user_name>/', views.user_profile_view, name='user_profile_view'),
    path("profile/<str:username>/saved-planets/", views.saved_planets_in_profile, name="saved_planets"),
        path("reset_password/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html",
             email_template_name="accounts/password_reset_email.html",
             subject_template_name="accounts/password_reset_subject.txt",
             success_url=reverse_lazy("accounts:password_reset_done")
         ),
         name="reset_password"),

    path("reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"
         ),
         name="password_reset_done"),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_form.html",
            success_url=reverse_lazy("accounts:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),

    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"
         ),
         name="password_reset_complete"),

]

