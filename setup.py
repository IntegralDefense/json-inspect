import setuptools

__version__ = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="json_inspect",
    version=__version__,
    author="Kyle Piper",
    author_email="kylepiper29@gmail.com",
    description="Inspects JSON logs for SIEM ingestion.",
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IntegralDefense/json-inspect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Security",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="logs",
)

# TO BE CONTINUED...
