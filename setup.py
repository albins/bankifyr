from setuptools import setup

import bankifyr

setup(
    name='bankifyr',

    # Uses semver
    version=bankifyr.__version__,

    description='Bank statement classification utility',
    long_description="",

    url='',

    # Author details
    author='Albin Stjerna, YOUR_NAMES_HERE',
    author_email='albin.stjerna@gmail.com, YOUR_EMAILS_HERE',
    license="GPLv3",
    packages=['bankifyr'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],

    install_requires=['matplotlib', 'nltk', 'daiquiri'],
    scripts=['bin/bankifyr'],
)
