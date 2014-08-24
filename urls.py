from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^(\d+)', 'core.views.show_post', name="show_post")
)
