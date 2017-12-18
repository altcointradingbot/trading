#!/usr/bin/env python2.7

"""Setup script."""

from setuptools import setup

setup(
    name="tradingbot",
    version="0.0.0",
    authors="Komarov Nikita, Ivan Shkurak, Alexandra Minochkina",
    url="https://github.com/altcointradingbot/trading",
    license="MIT",
    packages=[
        "tradingbot",
    ],
    install_requires=[
        "hashlib",
        "hmac",
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 1",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points = {
    'console_scripts':['altcointradingbot=tradingbot.run.run']
    }
)
