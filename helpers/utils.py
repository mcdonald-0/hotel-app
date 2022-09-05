from io import BytesIO

from PIL import Image

from django.core.files import File


def compress_image(image):
    img = Image.open(image)
    img = img.resize((int(img.size[0] * 0.7), int(img.size[1] * 0.7)), Image.ANTIALIAS)
    img_io = BytesIO()

    try:
        img.save(img_io, "JPEG", quality=40, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(img_io, "JPEG", quality=40, optimize=True)

    new_image = File(img_io, name=image.name)
    return new_image

# Todo: create a while loop that keeps looping untill the image is compressed to less than 1MB
