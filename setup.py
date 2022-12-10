import os
from setuptools import setup

install_requires = [
    ('kafka-python', '2.0.2'),
    ('flake8', '5.0.4'),
    ('pydantic', '1.10.2'),
    ('python-dotenv', '0.21.0'),
    ('APScheduler', '3.9.1.post1'),
    ('psycopg2-binary', '2.9.5'),
    ('requests', '2.27.1'),
    ('beautifulsoup4', '4.11.1'),
    ('stix2-elevator', '4.1.7'),
    ('stix2', '3.0.1'),
    ('flatdict', '4.0.1'),
    ('dagster', '1.0.17'),
    ('dagit', '1.0.17'),
    ("alembic", "1.8.1"),
    ("flask-restplus", "0.13.0"),
    ("Flask", "1.1.2"),
    ('Flask-WTF', '1.0.1')
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "events-collector").replace("-", "_")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Коллектор событий")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.in.axept.com/rshb/events-collector")
CI_FLASK_NAME = os.environ.get("CI_FLASK_NAME", "flask-app").replace("-", "_")
FLASK_APP = os.environ.setdefault("FLASK_APP", "src/eventscollector/web/app.py")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.9.1",
    entry_points={
        'console_scripts': [ 
            CI_PROJECT_NAME + " = " + "eventscollector:main",
            CI_FLASK_NAME + " = " + "eventscollector.web:app"

        ]
    }
)
