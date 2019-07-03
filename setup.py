#!/usr/bin/env
# -*- coding: utf-8 -*-
"""Setup"""

import setuptools

with open("README.md") as file:
    long_description = file.read()

setuptools.setup(
    author="Daniel Henrysson",
    author_email="henrysson.daniel@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Teacup visualization back-end written in Python",
    install_requires=[
        'flask', 'flask-cors', 'Flask-Session', 'itsdangerous', 'requests'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="teacup-visualization-back",
    packages=setuptools.find_packages(),
    url="https://github.com/HenryssonDaniel/teacup-visualization-web-back-python",
    version="1.0.0"
)
