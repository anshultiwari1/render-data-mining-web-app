# -*- coding: utf-8 -*-
"""
Author  : Anshul Tiwari
Date    : Jan 21, 2015

Description : This holds the URL Description.
"""

from django.conf.urls.defaults import patterns, include, url
import rpc
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views.applauncher import ShotView

urlpatterns = patterns('',
    (r'^jsonrpc$', rpc.jsonrpc_handler),
    # Examples:
    # url(r'^$', 'shotApp.views.home', name='home'),
    # url(r'^shotApp/', include('shotApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^accounts/login/$',  'views.login_view'),
    #(r'^accounts/logout/$', 'views.logout_view'),

    url(r'^shotApp/$', ShotView.as_view()),
    url(r'^$', ShotView.as_view()),
    #url(r'^user/(\w+)$', ShotView.as_view()),
    #url(r'^seq/(\.*)$', ShotView.as_view()),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': False}),

)
