import os
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


class WriteForUsView(View):
    template_name = "pages/write_for_us.html"

    CATEGORY_CHOICES = [
        "Politics", "Finance", "Tech", "Travel",
        "Celebrities", "Food", "Make-Up", "Marketing", "World",
    ]

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"categories": self.CATEGORY_CHOICES})

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        category = request.POST.get("category", "").strip()
        article_title = request.POST.get("article_title", "").strip()
        pitch = request.POST.get("pitch", "").strip()
        portfolio_url = request.POST.get("portfolio_url", "").strip()
        honeypot = request.POST.get("website", "").strip()
        uploaded_file = request.FILES.get("writing_sample")

        form_data = {
            "full_name": full_name,
            "email": email,
            "category": category,
            "article_title": article_title,
            "pitch": pitch,
            "portfolio_url": portfolio_url,
        }

        if honeypot:
            logger.warning(
                "Write For Us form honeypot triggered from IP %s",
                request.META.get("REMOTE_ADDR"),
            )
            messages.success(request, "Thanks for your pitch! Our editorial team will review it shortly.")
            return redirect("WriteForUsPage")

        errors = []
        if not full_name:
            errors.append("Please enter your full name.")
        if not email:
            errors.append("Please enter your email address.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a valid email address.")
        if not category or category not in self.CATEGORY_CHOICES:
            errors.append("Please select a valid category.")
        if not article_title:
            errors.append("Please enter a proposed article title.")
        if not pitch:
            errors.append("Please tell us about your article idea.")
        elif len(pitch) > MAX_MESSAGE_LENGTH:
            errors.append(f"Pitch is too long ({MAX_MESSAGE_LENGTH} characters max).")

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ALLOWED_SAMPLE_EXTENSIONS:
                errors.append("Writing sample must be a PDF, DOC, DOCX, or TXT file.")
            if uploaded_file.size > MAX_SAMPLE_FILE_SIZE_MB * 1024 * 1024:
                errors.append(f"Writing sample must be smaller than {MAX_SAMPLE_FILE_SIZE_MB}MB.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(
                request,
                self.template_name,
                {"form_data": form_data, "categories": self.CATEGORY_CHOICES},
                status=400,
            )

        email_body = (
            'New "Write For Us" submission for Gen Voice News\n\n'
            f"Name: {full_name}\n"
            f"Email: {email}\n"
            f"Category: {category}\n"
            f"Proposed Title: {article_title}\n"
            f"Portfolio / Samples link: {portfolio_url or '—'}\n\n"
            f"Pitch:\n{pitch}\n"
        )

        try:
            mail = EmailMessage(
                subject=f"[Write For Us] {article_title}",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.WRITER_SUBMISSIONS_EMAIL],
                reply_to=[email],
            )
            if uploaded_file:
                # Attached directly from memory — never written to disk,
                # so no storage/model is needed for this.
                mail.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
            mail.send(fail_silently=False)
        except BadHeaderError:
            messages.error(request, "Invalid header detected in your submission. Please try again.")
            return render(
                request,
                self.template_name,
                {"form_data": form_data, "categories": self.CATEGORY_CHOICES},
                status=400,
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to send write-for-us email: %s", exc)
            messages.error(request, "Something went wrong submitting your pitch. Please try again shortly.")
            return render(
                request,
                self.template_name,
                {"form_data": form_data, "categories": self.CATEGORY_CHOICES},
                status=500,
            )

        messages.success(
            request,
            "Thanks for your pitch! Our editorial team reviews submissions within 5–7 business days.",
        )
        return redirect("WriteForUsPage")