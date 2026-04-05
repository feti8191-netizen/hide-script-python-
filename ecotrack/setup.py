"""Setup script for EcoTrack installation."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ecotrack",
    version="1.0.0",
    author="EcoTrack Contributors",
    author_email="eco@example.com",
    description="Carbon Footprint Calculator and Tracker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ecotrack",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Environmental Science",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ecotrack=src.ecotrack:main",
        ],
    },
)
