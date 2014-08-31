from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^(\d+)/$', 'core.views.show_post', name="show_post"),
    url(r'^vote/(?P<kind>.+)/(?P<pk>\d+)/$',
        'core.views.ballot_box', name="vote"),
    url(r'^login/', login, {'template_name': "login.html"}, name="login"),
    url(r'^logout/$', 'core.views.logout_view', name='logout'),
)
