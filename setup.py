from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.9",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.9:
- Simplified the initialization of the VoiceGatewayClient.
""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
