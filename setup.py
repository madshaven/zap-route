#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

''' Setup for ZapPy.
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zap-route",
    version="0.1.1",
    author="Inge Madshaven",
    author_email="inge.madshaven@gmail.com",
    description="An intuitive method of routing between pages in Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/madshaven/",  # todo: fixme
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['Python', 'Streamlit', ],
    # python_requires=">=3.6",
    # install_requires=[
    #     "streamlit >= 0.86",
    # ],
)
