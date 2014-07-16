# -*- coding: utf-8 -*-

import permissions
import logging
from zope.i18nmessageid import MessageFactory

logger = logging.getLogger('rt.lastmodifier')
_ = MessageFactory('rt.lastmodifier')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
