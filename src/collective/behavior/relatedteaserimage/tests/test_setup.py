# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.relatedteaserimage.testing import COLLECTIVE_BEHAVIOR_RELATEDTEASERIMAGE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.behavior.relatedteaserimage is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_RELATEDTEASERIMAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.behavior.relatedteaserimage is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.behavior.relatedteaserimage'))

    def test_browserlayer(self):
        """Test that ICollectiveBehaviorRelatedteaserimageLayer is registered."""
        from collective.behavior.relatedteaserimage.interfaces import (
            ICollectiveBehaviorRelatedteaserimageLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveBehaviorRelatedteaserimageLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_RELATEDTEASERIMAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.behavior.relatedteaserimage'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.behavior.relatedteaserimage is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.behavior.relatedteaserimage'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBehaviorRelatedteaserimageLayer is removed."""
        from collective.behavior.relatedteaserimage.interfaces import \
            ICollectiveBehaviorRelatedteaserimageLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveBehaviorRelatedteaserimageLayer,
            utils.registered_layers())
