# -*- coding: utf-8 -*-
"""
VideoWave is the package to create and superimpose audio waves over a video.

"""

import sys
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

if sys.version_info < (3, 5):
    raise EnvironmentError("Python version >= 3.5 required. Python 3.7 is recommended")

# Versioning
MAJOR       = 0
MINOR       = 2
MICRO       = 0
PRE_RELEASE = 'a'
VERSION = f"{MAJOR}.{MINOR}.{MICRO}-{PRE_RELEASE}"

DEFAULT_URL = 'https://github.com/Mayitzin/VideoWave/'

metadata = dict(
    name='VideoWave',
    version=VERSION,
    description='Audio Wave creator for video clips',
    long_description=long_description,
    url=DEFAULT_URL,
    download_url=DEFAULT_URL+'releases/',
    author='Mario Garcia',
    author_email='mariogc@protonmail.com',
    keywords="video audio signal processing visualization",
    project_urls={
        "Bug Tracker": DEFAULT_URL+"issues/"
    },
    install_requires=['numpy',
                      'scipy',
                      'matplotlib',
                      'opencv-python'],
    packages=find_packages()
)

setup(**metadata)
