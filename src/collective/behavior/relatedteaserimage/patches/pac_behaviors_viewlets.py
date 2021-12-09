# -*- coding: utf-8 -*-
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets import ViewletBase


def LeadImageViewlet_update(self):
    self.context = ILeadImage(self.context)
    self.available = True if getattr(self.context, 'image', False) else False
