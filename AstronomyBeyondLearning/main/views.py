from django.shortcuts import render , redirect
from .models import ContactMessage
from django.contrib import messages
from django.core.paginator import Paginator
from main.mailer import send_email
from django.conf import settings
from planets.models import Planet





def home(request):
    planets = Planet.objects.all()


    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")
        terms = request.POST.get("terms")

        if not terms:
            messages.error(request, "You must accept the terms.")
            return redirect("main:home")

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message_text,
            accepted_terms=True
        )

        html_content = f"""
        <h2>Hello {first_name},</h2>
        <p>Thank you for contacting us!</p>
        <p>We have received your message and our team will reply soon.</p>
        <br>
        <p>Best regards,<br><strong>ABL Team</strong></p>
        """

        send_email(
            to=email,
            subject="Your message has been received",
            html_content=html_content
        )


        messages.success(request, "Your message has been sent successfully!")
        return redirect("main:home")

    return render(request, "main/home.html", {"planets": planets})




def about_view(request):
    return render(request, "main/about.html")


def contact_messages_view(request):

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view this page.")
        return redirect("accounts:sign_in")

    if not request.user.is_staff and not request.user.has_perm("main.view_contactmessage"):
        messages.error(request, "You do not have permission to view this page.")
        return redirect("home")

    all_msgs = ContactMessage.objects.all().order_by("-created_at")

 
    ContactMessage.objects.filter(is_read=False).update(is_read=True)

    paginator = Paginator(all_msgs, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "main/contact_messages.html", {
        "page_obj": page_obj,
        "msgs": page_obj,
        "count": all_msgs.count(),
        "paginator": paginator,
    })

def error_404_view(request, exception):
    return render(request, "404.html", status=404)


