import os
from setuptools import setup, find_packages

install_requires = [
    ('kafka-python', '2.0.2'),
    ('flake8', '5.0.4'),
    ('pydantic', '1.10.2'),
    ('python-dotenv', '0.21.0'),
    ('psycopg2-binary', '2.9.5'),
    ('sqlalchemy', '1.4.44'),
    ('stix2-elevator', '4.1.7'),
    ('stix2', '3.0.1'),
    ('Flask', '1.1.2'),
    ('Flask-WTF', '1.0.1'),
    ('flask-cors', '3.0.10'),
    ('prometheus-client', '0.16.0'),
    ('psutil', '5.9.4')
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "events-collector")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Коллектор событий")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.in.axept.com/rshb/events-collector")
PROJECT_ROOT_PATH = "events_collector"


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.10.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME + " = " + f"{PROJECT_ROOT_PATH}.main:execute",
        ]
    },
    include_package_data=True,
    package_data={
        f"{PROJECT_ROOT_PATH}.config": ["config.ini"],
    },
)
