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
        'Flask==0.10.1',
        'Jinja2==2.7.2',
        'MarkupSafe==0.23',
        'Werkzeug==0.9.4',
        'gevent==20.5.0',
        'greenlet==0.4.15',
        'itsdangerous==0.24',
        'gunicorn==19.0',
        'ujson==5.4.0'
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
