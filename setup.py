#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, sys

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(HERE, 'scheduler'))

def main():
    setup_args = dict(
        name="scheduler",
        version="0.6.0",
        description="Message distributed center",
        author="CannedFish Liang",
        author_email="lianggy0719@126.com",
        url="https://github.com/CannedFish/scheduler",
        platforms="Linux",
        license="BSD",
        packages=find_packages(),
        install_requires=['pika==0.10.0', 'requests>=2.7.0'],
        package_data={},
        entry_points={
            'console_scripts': [
                'scheduler = scheduler.main:main',
                'test_send_msg = scheduler.test.test_send_msg:main'
            ]
        }
    )
    setup(**setup_args)

if __name__ == '__main__':
    main()

