from setuptools import setup, find_packages

setup(
    name="aa-discord-voicesnapshot",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"aa_discord_voicesnapshot": ["templates/aa_discord_voicesnapshot/*.html"]},
    install_requires=["requests"],
    description="Alliance Auth plugin to snapshot Discord voice channel occupants",
    author="FrFrmPukin",
    url="https://github.com/frfrmpukin/aa-discord-voicesnapshot",
)
