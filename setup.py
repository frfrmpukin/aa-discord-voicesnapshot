from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.13" packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.13:
gateway: defer Django model imports and resolve token at runtime

- Defer importing aa_discord_voicesnapshot.models until runtime to allow
  importing the package in non-Django contexts (tests, debug harness).
- Resolve Discord token from DISCORD_TOKEN env var or settings.DISCORD_BOT_TOKEN.
- Allow explicit token injection via VoiceGatewayClient(token=...).
- Add minimal logging for token prefix and guild id.

""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
