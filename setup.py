# -*- coding: utf-8 -*-
"""Installer for the rt.lastmodifier package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join(
    [open('README.rst').read(), open('docs/HISTORY.rst').read()]
)


setup(
    name='rt.lastmodifier',
    version='1.1.1',
    description="Extends features and shown data in Plone document byline section",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/redturtle/rt.lastmodifier',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/rt.lastmodifier',
        'Source': 'https://github.com/redturtle/rt.lastmodifier',
        'Tracker': 'https://github.com/redturtle/rt.lastmodifier/issues',
    },
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rt'],
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'collective.monkeypatcher',
        'plone.app.dexterity',
        'plone.api',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'pyquery',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = rt.lastmodifier.locales.update:update_locale
    """,
)
