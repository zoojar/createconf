"""setup"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="createconf",
    version="0.1.0",
    author="David Newton",
    author_email="david@davidjnewton.com",
    description="Create config files from templates and data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidjnewton/createconf",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "createconf=createconf:createconf_cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Mako>=1.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)
