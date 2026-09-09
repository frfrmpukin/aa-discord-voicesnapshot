from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.11",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.11:
- Added a new top‑level file
- Removed gateway startup from Django
- Added a Supervisor program (voicesnapshot) with logging
- Gateway now runs outside gunicorn

""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
