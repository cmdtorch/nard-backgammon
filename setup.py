#!/usr/bin/env python
from setuptools import setup, find_packages


# Parse version number from pyglet/__init__.py:
with open('nard_backgammon/__init__.py') as f:
    info = {}
    for line in f:
        if line.startswith('version'):
            exec(line, info)
            break


setup_info = dict(
    name='nard_backgammon',
    version=info['version'],
    author='Emil Humbatov',
    author_email='emil4154515@gmail.com',
    description='Classic board game of Nard (Backgammon) for two players.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cmdtorch/nard-backgammon',
    download_url=f'https://github.com/cmdtorch/nard-backgammon/archive/refs/tags/{info["version"]}.zip',
    license='MIT',

    project_urls={
        'Source': 'https://github.com/pyglet/pyglet',
        'Tracker': 'https://github.com/pyglet/pyglet/issues',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Topic :: Games/Entertainment :: Board Games",
    ],

    # Package info
    packages=['nard_backgammon'],
)

setup(**setup_info)