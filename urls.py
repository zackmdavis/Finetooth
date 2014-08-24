from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^(\d+)/$', 'core.views.show_post', name="show_post"),
    # TODO: `value` regex should support negative numbers 
    url(r'^vote/(?P<kind>.+)/(?P<pk>\d+)/(?P<value>\d+)/$',
        'core.views.ballot_box', name="vote"),
)
