from setuptools import setup
from sys import path

from fakelogs import __version__

path.insert(0, '.')

NAME = "fakelogs"

if __name__ == "__main__":

    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(
        name=NAME,
        version=__version__,
        author="Tony Rogers",
        author_email="tony.rogers@logdna.com",
        url="https://github.com/teriyakichild/fakelogs",
        license='ASLv2',
        packages=[NAME],
        package_dir={NAME: NAME},
        description="fakelogs - library for generating fake logs",

        install_requires=requirements,

        entry_points={
            'console_scripts': ['fakelogs = fakelogs.cli:main'],
        }
    )
