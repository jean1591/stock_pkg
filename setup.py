import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="stock_pkg",
    version="0.0.1",
    author="Jean Robertou",
    author_email="no_email@example.com",
    description="A Yahoo Finance API wrapper that use pandas and talib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jean1591/stock_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)