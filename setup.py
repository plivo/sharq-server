# -*- coding: utf-8 -*-
# Copyright (c) 2014 Plivo Team. See LICENSE.txt for details.
from setuptools import setup

setup(
    name='SharQServer',
    version='0.2.0',
    url='https://github.com/plivo/sharq-server',
    author='Plivo Team',
    author_email='hello@plivo.com',
    license=open('LICENSE.txt').read(),
    description='An API queuing server based on the SharQ library.',
    long_description=open('README.md').read(),
    packages=['sharq_server'],
    py_modules=['runner'],
    install_requires=[
        'SharQ==0.3.0',
        'Flask==0.10.1',
        'Jinja2==2.7.2',
        'MarkupSafe==0.23',
        'Werkzeug==0.9.4',
        'gevent==1.0.1',
        'greenlet==0.4.2',
        'itsdangerous==0.24',
        'wsgiref==0.1.2',
        'gunicorn==19.0',
        'ujson==1.33'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points="""
    [console_scripts]
    sharq-server=runner:run
    """
)
