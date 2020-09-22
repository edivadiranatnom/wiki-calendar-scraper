import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiki-calendar-scraper",
    version="0.0.1",
    author="Davide Montanari",
    author_email="davide.montanari10@gmail.com",
    description="Wiki Calendar Scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edivadiranatnom/wiki-calendar-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)