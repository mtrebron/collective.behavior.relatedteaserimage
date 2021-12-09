# -*- coding: utf-8 -*-
from plone import api
from Acquisition import aq_base
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ..behaviors.relatedteaserimage import IRelatedTeaserImageMarker
from ..behaviors.relatedteaserimage import IRelatedTeaserImageBehavior
from ..utils import get_linenumber
import logging

log = logging.getLogger(__name__)

class RelatedTeaserImageViewlet(ViewletBase):
    """ A simple viewlet which renders the related teaser image """

    template = ViewPageTemplateFile('./templates/viewlet_related_teaser_image.pt')


    def render(self):
        if '@@edit' in self.request.steps:
            return ''
        return self.index()


    def index(self):
        context = aq_base(self.context)
        if IRelatedTeaserImageMarker.providedBy(context):
            if context.related_image:
                return self.template()
        return ''


    def update(self):
        if IRelatedTeaserImageMarker.providedBy(self.context):
            self.context = IRelatedTeaserImageMarker(self.context)
            self.available = True if self.context.related_image else False
        else:
            self.available = False

        #log.info('%s - Teaser image viewlet: %s' % (self.context.getId(), self.available))


