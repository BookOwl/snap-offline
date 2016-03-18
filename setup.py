#!python3
from setuptools import setup
desc = '''
Offline Snap! runner and manager
'''

setup(
    name='localsnap',

    version="1.0.0",

    description='Offline Snap! runner and manager',
    long_description=desc,

    url='https://github.com/BookOwl/snap-offline',

    author='Matthew',
    author_email='Unknown',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Snap! downloader runner',

    py_modules=["localsnap"],

    install_requires=["requests",],

    entry_points={
    'console_scripts': [
        'localsnap=localsnap:main',
        ],
    },
)
