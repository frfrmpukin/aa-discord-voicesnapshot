from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.7",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "aa_discord_voicesnapshot": [
            "templates/aa_discord_voicesnapshot/*.html",
            "migrations/*.py",
        ]
    },
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.7:
- Edited MANIFEST.in to include missing file structure
""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)


