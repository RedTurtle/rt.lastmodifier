from setuptools import setup, find_packages
import os

version = '0.1'

tests_require = ['plone.app.testing', 'pyquery']

setup(name='collective.lastmodifier',
      version=version,
      description="Save and show user last modifier information on Plone contents",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov modifier',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/collective.lastmodifier',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'plone.indexer',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
