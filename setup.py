from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "websocket-client",
    ],
    description="""Alliance Auth plugin to snapshot Discord voice channel occupants

Changes in 1.0.8:
- Fixed packaging issues by removing package_data
- MANIFEST.in now correctly includes all module files
- Ensures AppConfig loads and gateway thread starts
""",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
