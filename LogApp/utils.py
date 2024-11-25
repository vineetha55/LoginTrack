# utils.py
from twilio.rest import Client
from django.conf import settings


def send_sms(to, message):
    """Send an SMS using Twilio to a list of numbers or a single number."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Check if 'to' is a list of phone numbers
    if isinstance(to, list):
        # If 'to' is a list, send SMS to each number
        for number in to:
            try:
                client.messages.create(
                    body=message,
                    from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio number
                    to=number  # Admin's phone number
                )
                print(f"SMS sent successfully to {number}.")
            except Exception as e:
                print(f"Failed to send SMS to {number}: {e}")
    else:
        # If 'to' is a single number, send SMS to that number
        try:
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio number
                to=to  # Admin's phone number
            )
            print("SMS sent successfully.")
        except Exception as e:
            print(f"Failed to send SMS: {e}")
