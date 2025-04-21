from setuptools import setup, find_packages

setup(
    name="regex_machine",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyparsing==3.1.4",
        "pycde==0.6.1",
    ],
)
