from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "aa_discord_voicesnapshot": [
            "templates/aa_discord_voicesnapshot/*.html"
        ]
    },
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.3:
- Added real-time Discord voice tracking via Gateway
- Added VoiceState model
- Added gateway listener thread
- Updated snapshot logic to use live voice data
- Fixed template rendering issues
""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)

