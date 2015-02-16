Changelog
=========

0.5.1 (unreleased)
------------------

- Fixed italian translation typo
  [keul] 


0.5.0 (2015-02-16)
------------------

- When visiting folders, show last modifier and modification date taken
  by most recent child document, not from folder itself
  [keul]

0.4.1 (2014-09-30)
------------------

- Fixed issue in calling ``@@manage-viewlets``, and generally
  accessing site root [keul]
- Fixed typo in italian translation [keul]

0.4 (2014-07-17)
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
