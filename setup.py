# File location: setup.py

from setuptools import setup, find_packages

setup(
    name='vidya : the dream of wonders',
    version='1.1.0',
    author='Rudra Pandey',
    author_email='warriorrudra2009@gmail.com',
    description='A modular and extensible AI assistant.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Rudra160113/vidya',
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=[
        # A list of core dependencies
        'numpy',
        'scipy',
        'pydub',
        'aiohttp',
        'aiohttp-cors',
        'requests',
        'cryptography',
        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'vidya=vidya.main:main',
        ],
    },
)
