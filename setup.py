#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = open('requirements.txt').read().splitlines()
test_requirements = open('tests/requirements.txt').read().splitlines()

setup(
    name='scrapy-mosquitera',
    version='0.1.1',
    url='https://github.com/scrapinghub/scrapy-mosquitera',
    description="Restrict crawl and scraping scope using matchers.",
    long_description=readme,
    author='Scrapinghub',
    author_email='info@scrapinghub.com',
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'scrapy_mosquitera': 'scrapy_mosquitera'},
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='mosquitera,scrapy-mosquitera',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
