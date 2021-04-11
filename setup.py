import setuptools

from nxarray._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nxarray",
    version=__version__,
    author="Mirco Panighel",
    author_email="mirkopanighel@gmail.com",
    description="xarray extension for NeXus input/output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nxarray/nxarray",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "xarray",
        "nexusformat",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
 
