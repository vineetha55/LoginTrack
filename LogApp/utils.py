# utils.py
from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    """Send an SMS using Twilio."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio number
            to=to  # Admin's phone number
        )
        print("SMS sent successfully.")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
