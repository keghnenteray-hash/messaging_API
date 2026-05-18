import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .serializers import EmailSerializer

# Create your views here.
logger = logging.getLogger(__name__)
 

class ContactView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        recipient_email = settings.CONTACT_RECIPIENT_EMAIL

        plain_body = (
            f"New Message from Contact Form\n"
            f"{"-" *40}\n"
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Subject: {data['subject']}\n"
            f"{"-" *40}\n"
            f"{data['message']}\n"
            f"{"-" *40}\n"
            f"Reply to: {data['email']}"
        )

        html_body = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;background:#f9f9f9;">
          <div style="background:#fff;border-radius:8px;padding:32px;box-shadow:0 2px 8px rgba(0,0,0,.08);">
            <h2 style="margin:0 0 4px;color:#1a1a1a;">📬 New Contact Form Message</h2>
            <p style="margin:0 0 24px;color:#666;font-size:14px;">Submitted via your website contact form</p>
            <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
              <tr><td style="padding:8px 0;color:#888;font-size:13px;width:80px;">Name</td>
                  <td style="padding:8px 0;color:#1a1a1a;font-weight:600;">{data['name']}</td></tr>
              <tr><td style="padding:8px 0;color:#888;font-size:13px;">Email</td>
                  <td style="padding:8px 0;"><a href="mailto:{data['email']}" style="color:#4f46e5;">{data['email']}</a></td></tr>
              <tr><td style="padding:8px 0;color:#888;font-size:13px;">Subject</td>
                  <td style="padding:8px 0;color:#1a1a1a;">{data['subject']}</td></tr>
            </table>
            <div style="background:#f4f4f5;border-radius:6px;padding:16px;">
              <p style="margin:0;color:#1a1a1a;white-space:pre-wrap;line-height:1.6;">{data['message']}</p>
            </div>
            <p style="margin:24px 0 0;font-size:13px;color:#888;">
              Reply directly to <a href="mailto:{data['email']}" style="color:#4f46e5;">{data['email']}</a>
            </p>
          </div>
        </div>
        """

        try:
            send_mail(
                subject=f"[Contact Form] {data['subject']}",
                message=plain_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
                html_message=html_body,
                fail_silently=False,
            )

            logger.info(f"Contact form email sent from {data['email']}")
            return Response(
                {"detail": "Message sent successfully."},
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response(
                {"detail": "Failed to send message. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 