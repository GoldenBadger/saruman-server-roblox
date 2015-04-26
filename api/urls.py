# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^version$', views.version, name='version'),
    url(r'^init$', views.init, name='init'),
    url(r'^move$', views.move, name='move'),
)
