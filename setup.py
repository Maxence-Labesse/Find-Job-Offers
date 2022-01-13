from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Find-Job-Offers',
    version='1.0.0',
    description="Software to collect job offers and main informations from indeed.fr",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Maxence-Labesse/Find-Job-Offers',
    author='Maxence LABESSE',
    author_email="maxence.labesse@yahoo.fr",
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["src", "src.utils"]
)
