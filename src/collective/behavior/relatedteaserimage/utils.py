# -*- coding: utf-8 -*-
from plone import api
from zope.globalrequest import getRequest
from Products.CMFPlone.interfaces import ILanguage

from inspect import currentframe
import logging

log = logging.getLogger(__name__)


def get_linenumber():
    """ see https://stackoverflow.com/questions/3056048/filename-and-line-number-of-python-script
    """
    cf = currentframe()
    return cf.f_back.f_lineno


def default_pattern_options(context=None):

    portal = api.portal.get()

    # can this actually happen?
    if not context:
        request = getRequest()
        context = request.PARENTS[0]

    language = ILanguage(context).get_language()

    # this should return the portal if plone.app.multilingual is not installed
    language_root = portal.get(language, portal)

    favorite_items = [{
          'title': language_root.title_or_id()
        , 'path': '/'.join(language_root.getPhysicalPath())
        , }]

    more_items = api.content.find(
          context=language_root
          , portal_type = ['Folder', 'LIF']
          , depth=1
          , sort_on='sortable_title'
          , )

    for item in more_items:
        # restrict to assets folders
        if 'assets' in item.getId:
            favorite_items.append({
                'title': item.Title
            , 'path' : item.getPath()
            , })

    return favorite_items


def default_base_path(context=None):

    portal = api.portal.get()

    # can this actually happen?
    if not context:
        request = getRequest()
        context = request.PARENTS[0]

    language = ILanguage(context).get_language()

    # this should return the portal if plone.app.multilingual is not installed
    language_root = portal.get(language, portal)

    root_path = '/'.join(language_root.getPhysicalPath())

    return root_path

