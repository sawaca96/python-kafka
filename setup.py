# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "trading",
    "trading.utils",
]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": "trading",
    "version": "0.1.0",
    "description": "",
    "long_description": None,
    "author": "cairo",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": None,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
