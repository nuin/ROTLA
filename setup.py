#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
]

setup(
    name='ROTLA',
    version='2.0.1',
    python_requires='>=3.8',
    description="Split-read mapper for detecting mitochondrial deletions",
    long_description=readme + '\n\n' + history,
    author="Christopher Andrew Lavender, Adam Burkholder",
    author_email='c.andrew.lavender@gmail.com, adam.burkholder@nih.gov',
    url='https://github.com/NIEHS/ROTLA',
    packages=find_packages(include=['ROTLA']),
    entry_points={
        'console_scripts': [
            'ROTLA=ROTLA.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ROTLA',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    data_files=[('config', ['paths.cfg'])],
)
