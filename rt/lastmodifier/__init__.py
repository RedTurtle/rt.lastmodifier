# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
from rt.lastmodifier import permissions  # noqa

import logging

logger = logging.getLogger('rt.lastmodifier')
_ = MessageFactory('rt.lastmodifier')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
