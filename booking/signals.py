import logging

from io import BytesIO

from PIL import Image

from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save

from booking.models import RoomTypeImage


THUMBNAIL_SIZE = (350, 200)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=RoomTypeImage)
def generate_thumbnail(sender, instance, **kwargs):
    logger.info(f"Generating thumbnail for {instance.room_type.name} room at {instance.room_type.hotel.name}")

    image = Image.open(instance.image)
    image = image.convert("RGB")

    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_thumb = BytesIO()

    image.save(temp_thumb, "JPEG")

    temp_thumb.seek(0)
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )

    temp_thumb.close()
