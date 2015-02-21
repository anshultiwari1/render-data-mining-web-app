# -*- coding: utf-8 -*-
"""
Author  : Anshul Tiwari
Date    : Jan 21, 2015

Description : This holds the view.
"""
import settings
import sys

from django.utils.decorators        import method_decorator
from django.http                    import HttpResponse
from django.views.generic.base      import TemplateResponseMixin
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.contrib.contenttypes        import generic
from django.contrib.contenttypes.models import ContentType
from django.core        import serializers
from django.core.mail   import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.db          import IntegrityError
from django.db          import models
from django.db.models   import Q
from django.db.models   import Sum
from django.db.models.signals import post_save
from django.dispatch    import receiver
from django.utils       import simplejson
from django.shortcuts import render
from django.core.serializers import json
from json import dumps


class ShotView( TemplateView ):
	def __init__(self):
		super(ShotView, self).__init__()

	def dispatch(self, request, name=None, *args, **kwargs):
                print >>sys.stderr, "name: ", name
                if name is None:
		    self.template_name = "shotApp.html"
                else:
                    self.template_name = "shotApp2.html"
		return super(ShotView, self).dispatch(request, *args, **kwargs)

	'''def get_context_data(self, **kwargs):
		context = super(WelcomeView, self).get_context_data(**kwargs)
		context['login'] = self.request.user
		return context'''
