from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'Finetooth.core.views.home', name='home'),
)
