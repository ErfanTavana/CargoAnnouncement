from django.shortcuts import render
from .models import Captcha
from django.utils import timezone

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
        captcha = Captcha.objects.get(id=id_captcha, is_valid=True, expires_at__gt=timezone.now())
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


# Function to create a new captcha
def create_captcha(request):
    """
    Create and return a random Captcha.

    Filters used for data retrieval:
        Expired captchas are filtered, and associated images are deleted.

    Threading Purpose:
        To retrieve and delete expired captchas and their associated images concurrently using a separate thread.

    Captcha Generation Steps:
        1. Start a thread to clean up expired captchas.
        2. Generate a random Captcha.
        3. Save the Captcha.
        4. Return the Captcha details as a JSON response.

    Returns:
        JsonResponse: Response containing a success message, Captcha details, and guide.
    """
    # Retrieve and delete expired captchas and their associated images using a separate thread
    cleanup_thread = threading.Thread(target=cleanup_expired_captchas)
    cleanup_thread.start()

    # Generate a random Captcha, save it, and return its details as a JSON response
    captcha = Captcha.generate_random_captcha()
    captcha.save()
    return JsonResponse(
        {'message': "Captcha created", 'data': {'image': captcha.image.url, 'id': captcha.id}, 'guide': captcha.guide},
        status=200)
