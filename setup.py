import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="elite-dangerous-classes-library",
    version="1.0.0",
    url="https://github.com/MKaras93/elite-dangerous-classes-library",
    author="Michal Karas",
    packages=find_packages(exclude=("tests",)),
)
