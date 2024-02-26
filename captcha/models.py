from django.db import models
import os
import random
import string
import datetime
from django.contrib.auth.models import User
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from django.utils import timezone
from django.conf import settings
from io import BytesIO


# Function to generate a complex ID consisting of letters and numbers
def generate_complex_id():
    """
    Generate a complex ID consisting of letters and numbers.

    Returns:
        str: The generated complex ID.
    """
    id_length = 18  # Length of the generated complex ID
    characters = string.ascii_letters + string.digits  # Set of characters (letters and digits) to choose from
    complex_id = ''.join(
        random.choice(characters) for _ in range(id_length))  # Generate the complex ID using random characters
    return complex_id  # Return the generated complex ID


# Captcha Class
class Captcha(models.Model):
    # Unique identifier for the captcha
    id = models.CharField(primary_key=True, default=generate_complex_id, max_length=18, unique=True)
    # Image field to store the captcha image
    image = models.ImageField(blank=True, null=True)
    # Text associated with the captcha
    text = models.CharField(max_length=200, blank=True, null=True)
    # Guide or hint for the user regarding the captcha
    guide = models.CharField(max_length=200, blank=True, null=True)
    # Answer to the captcha
    answer = models.CharField(max_length=200, blank=True, null=True)
    # Flag indicating whether the captcha is valid
    is_valid = models.BooleanField(default=True, auto_created=True)
    # Timestamp for when the captcha was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the captcha expires
    expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to set timestamps and generate captcha on save.
        """
        # If the captcha is not created yet, set the created_at timestamp
        if not self.created_at:
            self.created_at = timezone.now()

        # Set the expiration timestamp for the captcha
        self.expires_at = self.created_at + datetime.timedelta(minutes=3)

        # Call the original save method
        super().save(*args, **kwargs)

    def generate_text_captcha(self):
        """
        Generate a text-based captcha image.
        """
        width, height = 200, 100
        captcha_image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(captcha_image)

        # Number of random points
        num_points = 1800
        # Color of the points
        point_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for _ in range(num_points):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=point_color)

        # Characters for the captcha
        characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        captcha_text = ''.join(random.choice(characters) for _ in range(6))

        # Load font (try Arial, fallback to DejaVuSans for Linux)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.truetype("DejaVuSans.ttf", 36)  # font for Linux

        for i in range(6):
            char_x = 10 + i * 30
            char_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.text((char_x, 30), captcha_text[i], fill=char_color, font=font)

        # Save image and update model fields
        image_buffer = BytesIO()
        captcha_image.save(image_buffer, format="PNG")
        image_name = f"{random.randint(1, 100000)}.png"
        self.image.save(image_name, content=BytesIO(image_buffer.getvalue()), save=False)
        self.text = captcha_text
        self.answer = captcha_text
        self.guide = 'Enter the text from the image'
        super().save()

    def generate_math_captcha(self):
        """
        Generate a math-based captcha image.
        """
        width, height = 200, 100
        captcha_image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(captcha_image)

        # Generate random numbers and operation
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(["+", "-", "×"])

        # Calculate result based on operation
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        else:
            result = num1 * num2

        # Create text for the captcha
        num1_str = str(num1)
        num2_str = str(num2)
        text = f'{num1_str} {operation} {num2_str} ='

        # Number of random lines
        num_random_lines = 8

        for _ in range(num_random_lines):
            line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=line_color, width=2)

        # Colors for numbers and operation
        num_colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ]

        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.truetype("DejaVuSans.ttf", 36)  # font for Linux
        draw.text((10, 30), num1_str, fill=num_colors[0], font=font)
        draw.text((60, 30), operation, fill=num_colors[1], font=font)
        draw.text((110, 30), num2_str, fill=num_colors[2], font=font)
        draw.text((160, 30), '=', fill=num_colors[1], font=font)

        # Save image and update model fields
        image_buffer = BytesIO()
        captcha_image.save(image_buffer, format="PNG")
        image_name = f"{random.randint(1, 100000)}.png"
        self.image.save(image_name, content=BytesIO(image_buffer.getvalue()), save=False)
        self.text = text
        self.answer = str(result)
        self.guide = 'Enter image math operations'
        super().save()

    @classmethod
    def generate_random_captcha(cls):
        """
        Generate a random captcha (either text or math) and return an instance of Captcha.

        Returns:
            Captcha: An instance of the generated captcha.
        """
        # Create a new instance of Captcha
        captcha = cls()

        # Randomly choose between text and math captchas
        if random.choice([True, False]):
            captcha.generate_text_captcha()
        else:
            captcha.generate_math_captcha()

        # Return the generated captcha instance
        return captcha
