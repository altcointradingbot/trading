#!/usr/bin/env python2.7

"""Setup script."""

from setuptools import setup
import os
setup(
    name="tradingbot",
    version="0.0.0",
    authors="Komarov Nikita, Ivan Shkurak, Alexandra Minochkina",
    url="https://github.com/altcointradingbot/trading",
    license="MIT",
    packages=[
        "tradingbot",
        "tradingbot.algorithms",
        "tradingbot.configs",
        "tradingbot.databases",
        "tradingbot.deciders",
        "tradingbot.examples",
        "tradingbot.exchangers",
        "tradingbot.exchangers_api",
        "tradingbot.third_party",
        "tradingbot.utils",
        "tradingbot.data",
    ],
    install_requires=[
        "hashlib",
        "hmac",
    ],
    package_data={"tradingbot.configs": ["DB_tables_description.json", "keys.txt", "livecoin_config.json"],
                  "tradingbot.data": ["collectiong.csv", "data.db", "livecoin.db", "livecoin.txt"]},
    include_package_dir=True,
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
    entry_points={
        'console_scripts': ['altcointradingbot=tradingbot.run:main']
    }
)
