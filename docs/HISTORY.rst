Changelog
=========

1.1.0 (2020-03-07)
------------------

- Python3 compatibility [cekk]


1.0.2 (2015-12-16)
------------------

- Fix document by line folder viewlet to take last modifier
  from last modified content inside the folder
  [fdelia]


1.0.1 (2015-10-16)
------------------

- Added memoize for caching the values of last_modifier method
  [fdelia]


1.0.0 (2015-09-07)
------------------

- Added a new permission ``rt.lastmodifier: show long time format``.
  This can enable/disable the full time format on dates.
  [keul]
- Added the ``ILastModifierInertContent`` marker interface for disable
  byline section on contents
  [keul]
- Fixed to byline infos: prevented some commas to be misdisplayed
  [keul]



0.6.0 (2015-07-28)
------------------

- Fixed italian translation typo
  [keul]
- Now save last modifier info in a low level annotation.
  This way we can have this information also when the content type do not
  use any versioning support (that is still the fallback)
  [keul]
- Do not, never, display any byline on site root.
  It's totally useless
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
