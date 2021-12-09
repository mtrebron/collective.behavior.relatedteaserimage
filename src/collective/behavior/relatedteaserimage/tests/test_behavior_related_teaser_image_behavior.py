# -*- coding: utf-8 -*-
from collective.behavior.relatedteaserimage.behaviors.related_teaser_image_behavior import IRelatedTeaserImageBehaviorMarker
from collective.behavior.relatedteaserimage.testing import COLLECTIVE_BEHAVIOR_RELATEDTEASERIMAGE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class RelatedTeaserImageBehaviorIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_RELATEDTEASERIMAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_related_teaser_image_behavior(self):
        behavior = getUtility(IBehavior, 'collective.behavior.relatedteaserimage.related_teaser_image_behavior')
        self.assertEqual(
            behavior.marker,
            IRelatedTeaserImageBehaviorMarker,
        )
