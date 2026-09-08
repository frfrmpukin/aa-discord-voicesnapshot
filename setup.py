from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.10",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.10:
- Connect start_gateway function to post_migrate signal to initiate VoiceGatewayClient after migrations.
""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
