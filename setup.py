from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.12",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.12:
- Edited README.md with more and better instructions.
- Made voicesnapshot_runner.py availabe for download and directions on where to place.

""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
