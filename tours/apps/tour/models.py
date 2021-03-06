# file tours/apps/tour/models.py

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.core.files import File
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import Max
from django import forms
from django.core.validators import ValidationError, RegexValidator, MaxLengthValidator, URLValidator

# third party imports
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from PIL import Image
import tempfile

import re
import os

from cStringIO import StringIO

def validate_twitter(value):
    if '@' in value:
        raise ValidationError('Do not include the @ in your Twitter Account')

class DirectionsMode(models.Model):
    mode = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % (self.mode)

class Tour(models.Model):
    name = models.CharField(max_length=50)
    published = models.BooleanField(default=False)
    description = HTMLField()
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    mode = models.ForeignKey(DirectionsMode, default=1)
    fb_app_id = models.CharField(max_length=50, blank=True)
    fb_page_id = models.CharField(max_length=50, blank=True)
    twitter_acct = models.CharField(max_length=50, blank=True, validators=[validate_twitter])
    google_analytics = models.TextField(blank=True, default='')
    splashimage = models.ImageField(upload_to='tours/', blank=True, default='')

    class Meta:
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')

    def __unicode__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return "%s" % (self.name)

class TourInfo(models.Model):
    tour = models.ForeignKey(Tour)
    name = models.CharField(max_length=50)
    description = HTMLField(blank=True, default='')
    position = models.PositiveSmallIntegerField("Position", default=1)
    info_slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    class Meta:
        verbose_name = _('Tour Info')
        verbose_name_plural = _('Tour Info')

        #set default ordering for the manager
        ordering = ['position']

    def __unicode__(self):
        return "%s - %s" % (self.name, self.tour.name)

    def get_absolute_url(self):
        return reverse('tour:info-detail', kwargs={"slug":  self.tour.slug, "info": self.info_slug})

def new_position(instance, tour_id):
    return TourStop.objects.filter(tour_id=tour_id).count()

def validate_https(value):
    if 'https' not in value:
        raise ValidationError('Make sure your embed link uses HTTPS.')

class TourStop(models.Model):
    tour = models.ForeignKey(Tour)
    name = models.CharField(max_length=50)
    description = HTMLField(blank=True, default='')
    metadescription = models.TextField(blank=True, default='', validators=[MaxLengthValidator(350)])
    article_link = models.CharField(max_length=525, blank=True, default='')
    video_embed = models.CharField(max_length=50, blank=True, default='', validators=[URLValidator(), validate_https])
    # geo fields
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    park_lat = models.FloatField(null=True, blank=True)
    park_lng = models.FloatField(null=True, blank=True)
    parking_block = models.TextField(blank=True, default='')

    direction_notes = HTMLField(blank=True, default='')

    # used in drag and drop reodering as well as tour stop order
    position = models.PositiveSmallIntegerField("Position", blank=True, null=True, default='')

    class Meta:
        verbose_name = _('Tour Stop')
        verbose_name_plural = _('Tour Stops')

        #set default ordering for the manager
        ordering = ['position']

    def __unicode__(self):
        return "%s - %s" % (self.name, self.tour.name)

    def get_absolute_url(self):
        return reverse('tour:stop-detail', kwargs={"slug":  self.tour.slug, "page": self.position + 1})

    @property
    def slug(self):
        return slugify(self.name)

    def save(self, force_insert=False, force_update=False):
        if self.position == None:
            self.position = new_position(self, self.tour_id)
        super(TourStop, self).save(force_insert, force_update)

class TourStopMedia(models.Model):
    tour_stop = models.ForeignKey(TourStop)
    title = models.CharField(max_length=50, blank=True, default='')
    caption = models.CharField(max_length=255, blank=True, default='')
    image = models.ImageField(upload_to='stops/', verbose_name='Image')
    inline = models.ImageField(upload_to='stops/inline/', blank=True, null=True)
    source_link = models.CharField(max_length=525, blank=True, default='')
    metadata = HTMLField(blank=True, default='')

    class Meta:
        verbose_name = _('Tour Stop Media')
        verbose_name_plural = _('Tour Stop Media')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tour:stop-media-detail', kwargs={"slug":  self.tour_stop.tour.slug, "id": self.id})

    def save(self, *args, **kwargs):
        # override save method to resize image and generate thumbnail

        image_update = False
        # if pk is set, this is an update to an existing model;
        # check if the image is being changed
        if self.pk:
            orig = TourStopMedia.objects.get(pk=self.pk)
            if self.image != orig.image:
                image_update = True

        if self.image and not self.inline or image_update:
            self.generate_thumbnail()

        super(TourStopMedia, self).save(*args, **kwargs)

    def generate_thumbnail(self):
        thumbnail_size = (290, 290)
    
        return self._resize_imagefield(thumbnail_size, self.inline)

    def _resize_imagefield(self, size, field):
        image = Image.open(self.image)
        # NOTE: using thumbnail for both resize/thumb
        # because it resizes the current image rather than resize,
        # which returns a new Image object
        image.thumbnail(size, Image.ANTIALIAS)
        tmp = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp.name, 'png')
        content = File(tmp)
        field.save('%s' % self.image, content, save=False)

