Enhance the Plone adding an additional information on document view: the **user who performed the last change** and
the **change note**.
Optionally expands the **document byline** section showing those informations.

.. contents:: **Table of contents**

Documentation
=============

Plone already handle lot of infos in the document byline section, like the document author, the modification date
and the publication date.

In the same way new data added by this add-on will be added to the byline section.

.. image:: http://blog.redturtle.it/pypi-images/rt.lastmodifier/rt.lastmodifier-0.4-01.png
   :alt: Document byline preview in the Plone 4.3 style

When the new byline informations are shown?
-------------------------------------------

New infos apart, all byline elements can now be controlled with a **granular security configuration**.
This will change the way to handle document byline because commonly Plone simply use a couple of
site-wide options: the *allow_anon_views_about* and the *displayPublicationDateInByline*.

The viewlet will now handle many different informations: *author*, *last modifier*, *publication date*,
*modification date* and *last versioning change note*.
Each information is visible if the user has a specified permission:

- ``rt.lastmodifier: documentByLine view author``
- ``rt.lastmodifier: documentByLine view last modifier``
- ``rt.lastmodifier: documentByLine view modification date``
- ``rt.lastmodifier: documentByLine view publication date``
- ``rt.lastmodifier: documentByLine view change note``
- ``rt.lastmodifier: show long time format``

To show last modifier info, *Creator* and *Modifier* must be not equals (just for not show a duplicate link).

By default Anonymous users can't see anything (this will reproduce the Plone default behavior, where Anonymous
can't see the byline section by default).

The "show long time format" permission can enable disable the visibility of timing when dates are displayed.

Disabling byline on content types
---------------------------------

Sometimes the byline section is displayed on contents where you don't need it.

In that case you can apply (from ZMI) a marker interface named ``ILastModifierInertContent`` to a single
content, or let your 3rd-party content types to extends it.
This will disable the byline section.

Also, the byline section is automatically disabled on the Plone site root.

Show change notes
-----------------

This feature will show the comment to changes you did, that commonly are kept in the history section
so this only works for content type where `versioning`_ is activated.

The editor must explicitly choose if a change note must be putted in the byline section by selecting
the "*Show the changes note in document info*" checkbox.
This will store *that* change note to be shown in the content, that means that additional changes without
checking the option will not update that information.

.. image:: http://blog.redturtle.it/pypi-images/rt.lastmodifier/rt.lastmodifier-0.4-02.png
   :alt: New change note section

To *delete* the change note shown you must edit a document, provide an empty note while keeping the check
selected.

**Note**: this feature require JavaScript to work properly *and* has only be tested for Archetypes based
content types.

Installation
============

Add ``rt.lastmodifier`` to your buildout::

    [buildout]
    ...
    
    [instance]
    ...
    eggs=
       ...
       rt.lastmodifier

After that, install the "rt.lastmodifier" add-on product.

.. Note::
    Installation will trigger an index creation and population. This can require some times
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
  
  .. image:: http://www.fe.camcom.it/cciaa-logo.png/
     :alt: CCIAA Ferrara - logo
  
* `Province of Vicenza`__

  .. image:: http://www.provincia.vicenza.it/logo_provincia_vicenza.png
     :alt: Province of Vicenza - logo

All of them supports the `PloneGov initiative`__.

__ http://www.ospfe.it/
__ http://www.fe.camcom.it/
__ http://www.provincia.vicenza.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

.. _`versioning`: https://plone.org/documentation/manual/plone-4-user-manual/managing-content/versioning-plone-v3.3
