
from .models import Captcha
from django.utils import timezone
from rest_framework.response import Response
import threading
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import CaptchaSerializer


def captcha_validation(id_captcha, captcha_answer):
    """
    Validate the user's response to a captcha.

    Parameters:
    - id_captcha (int): The unique identifier of the captcha.
    - captcha_answer (str): The user's response to the captcha.

    Returns:
    - bool: True if the captcha is valid and the user's response is correct, False otherwise.
    """

    try:
        # Attempt to retrieve a valid captcha with the specified ID
        captcha = Captcha.objects.get(deleted_at=None, id=id_captcha, is_valid=True, expires_at__gt=timezone.now())
        # If correct, mark the captcha as invalid and save changes
        captcha.is_valid = False
        captcha.save()
        # Check if the user's response matches the captcha answer
        if captcha.answer == captcha_answer:
            return True
        else:
            return False
    except Captcha.DoesNotExist:
        # If captcha is not found, return False indicating validation failure
        return False


# Function to clean up expired captchas
def cleanup_expired_captchas():
    """
    Clean up expired captchas by deleting associated images and captcha records.

    Filters used for data retrieval: Expired captchas are filtered based on the 'expires_at' field.

    Loop Purpose:
        Iterate through the expired captchas to delete associated images and captcha records.
    """
    expired_captchas = Captcha.objects.filter(expires_at__lt=timezone.now())  # Retrieve expired captchas
    for captcha in expired_captchas:
        # Delete the associated image if it exists
        if captcha.image:
            captcha.image.delete()
        # Delete the captcha record
        captcha.delete()


# Function to generate and save a new captcha
def generate_new_captcha():
    """
    Generate a new random Captcha and save it.

    Captcha Generation Steps:
        1. Generate a random Captcha.
        2. Save the Captcha.

    Returns:
        Captcha: The generated Captcha instance.
    """
    cleanup_expired_captchas()
    captcha = Captcha.generate_random_captcha()
    captcha.save()
    return captcha
# Function to create a new captcha
@api_view(['GET'])
def create_captcha(request):
    captcha = generate_new_captcha()
    serializer = CaptchaSerializer(captcha, many=False)
    return Response({'message': 'کپچا با موفقیت ایجاد شد', 'data': serializer.data}, status=status.HTTP_200_OK)