from setuptools import setup, find_packages
import os

version = '0.4.dev0'

tests_require = ['plone.app.testing', 'pyquery']

setup(name='rt.lastmodifier',
      version=version,
      description="Greatly expand features and shown data in Plone document byline section",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov modifier catalog byline',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/rt.lastmodifier',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rt'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'plone.indexer',
          'archetypes.schemaextender',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
