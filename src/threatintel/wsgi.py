import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_CONFIGURATION", "BaseConfiguration")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.threatintel.settings")

application = get_wsgi_application()
