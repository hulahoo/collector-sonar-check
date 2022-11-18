import os
from setuptools import setup

setup(
    name=os.environ["CI_PROJECT_NAME"],
    version="0.0.1",
    description=os.environ["CI_PROJECT_TITLE"],
    url=os.environ["CI_PROJECT_URL"],
    install_requires=[
        "kafka-python>=2.0.2",
        "pydantic>=1.10.2",
        "loguru==0.6.0",
        "psycopg2-binary>=2.9.3",
        "requests>=2.27.1",
        "beautifulsoup4>=4.11.1",
        "stix2-elevator>=4.1.7",
        "stix2>=3.0.1",
        "flatdict>=4.0.1",
        "dagster>=1.0.17",
        "dagit>=1.0.17"
    ],
    entry_points={
        'console_scripts': [
            os.environ["CI_PROJECT_NAME"] +
            " = " +
            os.environ["CI_PROJECT_NAME"] +
            ":main"
        ]
    }
)
