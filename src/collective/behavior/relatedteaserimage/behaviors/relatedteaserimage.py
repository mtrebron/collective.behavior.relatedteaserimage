# -*- coding: utf-8 -*-
from collective.behavior.relatedteaserimage import _
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider

from plone.autoform import directives
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.contenttypes.behaviors.leadimage import ILeadImage

from z3c.relationfield.schema import RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.form.browser.text import TextFieldWidget
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from ComputedAttribute import ComputedAttribute

from ..utils import default_pattern_options
from ..utils import default_base_path
from ..utils import get_linenumber

import logging
log = logging.getLogger(__name__)


class IRelatedTeaserImageMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IRelatedTeaserImageBehavior(model.Schema):

    related_image = RelationChoice(
        title=_(u"Related Teaser Image"),
        description=_(u"Add a teaser image"),
        required=False,
        default=None,
        vocabulary='plone.app.vocabularies.Catalog'
        )

    image_caption = schema.TextLine(
        title=_(u'label_image_caption', default=u'Image Caption'),
        description=u'',
        required=False,
    )

    directives.widget(
        'related_image',
        RelatedItemsFieldWidget,
        pattern_options = {
            'recentlyUsed': True,
            'basePath'    : default_base_path,
            'mode'        : 'auto',
            'favorites'   : default_pattern_options,
            'folderTypes': ['Folder', 'LIF', 'LRF'],
            'selectableTypes' : ['Image'],
        }
    )
    directives.widget(
        'image_caption',
        TextFieldWidget,
    )

#alsoProvides(IRelatedTeaserImageBehavior['image_caption'], ILanguageIndependentField)
#alsoProvides(IRelatedTeaserImageBehavior['related_image'], ILanguageIndependentField)

@implementer(IRelatedTeaserImageBehavior)
@adapter(IRelatedTeaserImageMarker)
class RelatedTeaserImage(object):

    def __init__(self, context):
        self.context = context

    @property
    def related_image(self):
        if hasattr(self.context, 'related_image'):
            return self.context.related_image
        return None

    @property
    def image_caption(self):
        if hasattr(self.context, 'image_caption'):
            return self.context.image_caption
        return None

    @related_image.setter
    def related_image(self, value):
        self.context.related_image = value

    @image_caption.setter
    def image_caption(self, value):
        self.context.image_caption = value

    @ComputedAttribute
    def image(self):
        image_link = getattr(self.context.aq_explicit, 'related_image', False)
        linked_image = image_link and self.context.related_image.to_object.image or ''
        return linked_image


def addILeadImageInterface(context, event):
    context = getattr(context, 'aq_explicit', None)

    if context:
        has_image = getattr(context, 'related_image', False)
        if has_image and not ILeadImage.providedBy(context):
            alsoProvides(context, ILeadImage)
        elif not has_image:
            noLongerProvides(context, ILeadImage)
