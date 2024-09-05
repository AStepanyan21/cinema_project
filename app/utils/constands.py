import os

from app.configuration.settings import settings

MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), '../../media')
os.makedirs(MEDIA_FOLDER, exist_ok=True)
MEDIA_URL = f"{settings.app_settings.DOMAIN}/media/media/"