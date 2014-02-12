Enhance the Plone catalog adding an additional information: the **user who performed the last change**.
Optionally, expand the **document byline** section, showing this (and other) information.

.. contents:: **Table of contents**

Documentation
=============

Catalog changes
---------------

After installing this product, the catalog of your Plone site will be populated with a new index and a metadata
column: the ``Modifier``.
This will be the last user who performed a content change (both editing review state change).

Other products can start using this index for performing special searches.

Expand the document byline section
----------------------------------

Optionally, this new information can be added to the content's view.

.. image:: http://blog.redturtle.it/pypi-images/rt.lastmodifier/rt.lastmodifier-0.1-01.png
   :alt: Document byline preview

Please, note that this will also works for the new-style byline, that can also display the publication
date (see PLIP `#8699`__):

__ https://dev.plone.org/ticket/8699

.. image:: http://blog.redturtle.it/pypi-images/rt.lastmodifier/rt.lastmodifier-0.1-02.png
   :alt: Document byline preview in the Plone 4.3 style

In facts, this can backport the publication date feature to older Plone versions (but this is a side effect of
the product, not a wanted feature).

Apart publication date, all other by-line elements can now be controlled with a granular security settings.

When the new byline informations are shown?
-------------------------------------------

The viewlet handle 4 different informations: *author*, *last modifier*, *publication date* and *modification date*.
Each info is visible if the user has a specified permission on the context:

- ``rt.lastmodifier: documentByLine view author``
- ``rt.lastmodifier: documentByLine view last modifier``
- ``rt.lastmodifier: documentByLine view modification date``
- ``rt.lastmodifier: documentByLine view publication date``

This will change the way to handle document byline because commonly Plone simply use a couple of
site-wide options: the *allow_anon_views_about* and the *displayPublicationDateInByline*.

To show last modifier info, *Creator* and *Modifier* must be not equals (just for not show a duplicate link).

By default Anonymous users can't see anything (as Plone default).

Installation
============

Add ``rt.lastmodifier`` to your buildout:

.. code-block:: ini

    [buildout]
    ...
    
    [instance]
    ...
    eggs=
       ...
       rt.lastmodifier

After that, install the "rt.lastmodifier" add-on product.

.. Note::
    Installation will trigger the new index creation and population. This can require some times
    on huge sites.

Compatibility
-------------

All Plone versions from 3.3 to 4.3.

Credits
=======

Developed with the support of:

* `S. Anna Hospital, Ferrara`__
  
  .. image:: http://www.ospfe.it/ospfe-logo.jpg 
     :alt: S. Anna Hospital logo
  
* `Camera di Commercio di Ferrara`__

All of them supports the `PloneGov initiative`__.

__ http://www.ospfe.it/
__ http://www.fe.camcom.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
