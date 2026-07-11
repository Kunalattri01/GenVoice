import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, BadHeaderError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.views import View

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 5000
ALLOWED_SAMPLE_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
MAX_SAMPLE_FILE_SIZE_MB = 5

class ContactView(View):
    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_body = request.POST.get("message", "").strip()

        # Honeypot: a hidden field real users never fill in. Bots that
        # auto-fill every field will trip it.
        honeypot = request.POST.get("company_website", "").strip()

        form_data = {"name": name, "email": email, "subject": subject, "message": message_body}

        if honeypot:
            logger.warning(
                "Contact form honeypot triggered from IP %s",
                request.META.get("REMOTE_ADDR"),
            )
            # Pretend it worked so the bot doesn't learn anything — but send nothing.
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            return redirect("ContactPage")

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not email:
            errors.append("Please enter your email address.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a valid email address.")
        if not subject:
            errors.append("Please enter a subject.")
        if not message_body:
            errors.append("Please enter a message.")
        elif len(message_body) > MAX_MESSAGE_LENGTH:
            errors.append(f"Message is too long ({MAX_MESSAGE_LENGTH} characters max).")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, self.template_name, {"form_data": form_data}, status=400)

        email_body = (
            "New contact form submission from Gen Voice News\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message_body}\n"
        )

        try:
            mail = EmailMessage(
                subject=f"[Contact Form] {subject}",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECIPIENT_EMAIL],
                reply_to=[email],
            )
            mail.send(fail_silently=False)
        except BadHeaderError:
            messages.error(request, "Invalid header detected in your submission. Please try again.")
            return render(request, self.template_name, {"form_data": form_data}, status=400)
        except Exception as exc:  # noqa: BLE001 — catch any SMTP/network failure here
            logger.error("Failed to send contact email: %s", exc)
            messages.error(request, "Something went wrong sending your message. Please try again shortly.")
            return render(request, self.template_name, {"form_data": form_data}, status=500)

        messages.success(request, "Thanks for reaching out! We'll get back to you within 1–2 business days.")
        return redirect("ContactPage")


# =========================================================
# settings.py additions
# =========================================================

"""
DEFAULT_FROM_EMAIL = "no-reply@genvoicenews.com"
CONTACT_RECIPIENT_EMAIL = "hello@genvoicenews.com"
WRITER_SUBMISSIONS_EMAIL = "editorial@genvoicenews.com"

# Configure with your real SMTP provider (SendGrid, Mailgun, SES, etc.)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yourprovider.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-smtp-username"
EMAIL_HOST_PASSWORD = "your-smtp-password"

# django.contrib.messages must be enabled (it is, by default, in most
# Django projects) — MESSAGE_STORAGE defaults to the session backend,
# which is all this needs.
"""
