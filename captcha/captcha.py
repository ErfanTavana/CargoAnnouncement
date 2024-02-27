import os
import random
import string
import datetime
from PIL import Image, ImageDraw, ImageFont
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

# Function to generate a random captcha image
def generate_text_captcha():
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

    # Save image
    image_buffer = BytesIO()
    captcha_image.save(image_buffer, format="PNG")
    image_name = f"{random.randint(1, 100000)}.png"
    captcha_image.save(image_name, format="PNG")
    return image_name, captcha_text

# Function to generate a math-based captcha image
def generate_math_captcha():
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

    # Save image
    image_buffer = BytesIO()
    captcha_image.save(image_buffer, format="PNG")
    image_name = f"{random.randint(1, 100000)}.png"
    captcha_image.save(image_name, format="PNG")
    return image_name, text, str(result)

# Example usage
text_captcha_image_name, text_captcha_text = generate_text_captcha()
math_captcha_image_name, math_captcha_text, math_captcha_answer = generate_math_captcha()

print(f"Text Captcha Image Name: {text_captcha_image_name}")
print(f"Text Captcha Text: {text_captcha_text}")

print(f"Math Captcha Image Name: {math_captcha_image_name}")
print(f"Math Captcha Text: {math_captcha_text}")
print(f"Math Captcha Answer: {math_captcha_answer}")
