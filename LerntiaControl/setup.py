import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lerntia_control_pkg-saraheee",
    version="5.0.0",
    author="Sarah El-Sherbiny",
    author_email="sarah.el-sherbiny@tuwien.ac.at",
    description="Mouse control by tracking face and eyes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saraheee/LerntiaControl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.7',
)