from setuptools import setup, find_packages

setup(
    name="ctf-toolkit",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "requests",
        "beautifulsoup4",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "ctf-toolkit=main:app",  # <- das ist wichtig
        ],
    },
)