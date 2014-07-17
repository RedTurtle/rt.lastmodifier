Changelog
=========

0.4 (unreleased)
----------------

- New feature for showing the last change note on versionable contents.
  User must explicitly mark the change has "showable"
  [keul]

0.3.1 (2014-02-25)
------------------

- Fixed default roles: do not use ``Authenticated`` but ``Member``
  [keul]

0.3 (2014-02-12)
----------------

- Added new permissions to handle the view of single infos in the viewlet:
  author, last modifier, publication date and modified date
  [cekk]
- fixed bug: last modifier was never shown to anonymous users in Plone 4
  (`#1`__)
  [keul]

__ https://github.com/RedTurtle/rt.lastmodifier/issues/1

0.2 (2013-04-17)
----------------

* Renamed the product from "collective.lastmodifier" to "rt.lastmodifier".
  This is unbelievable and embarassing, but I didn't find `collective.lastmodifier`__ when I looked for
  a Plone product with those features... and in the end I choosed the same name!
  However the original product is using a different approach.
* Added collection criteria (for new and old ones)

__ https://pypi.python.org/pypi/collective.lastmodifier

0.1 (Unreleased)
----------------

- Initial release