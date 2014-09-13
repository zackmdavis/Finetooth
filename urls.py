from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login


urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^valuation_(-?\d+)-([0-9a-f]{6})_(-?\d+)-([0-9a-f]{6}).css$',
        'core.views.serve_stylesheet', name='stylesheet'),
    url(r'^(\d+)/$', 'core.views.show_post', name="show_post"),
    url(r'^new_post/$', 'core.views.new_post', name="new_post"),
    url(r'^tag/(\d+)/$', 'core.views.tag', name="tag"),
    url(r'^vote/(?P<kind>.+)/(?P<pk>\d+)/$',
        'core.views.ballot_box', name="vote"),
    url(r'^login/', login, {'template_name': "login.html"}, name="login"),
    url(r'^logout/$', 'core.views.logout_view', name='logout'),
    url(r'^signup/$', 'core.views.sign_up', name='sign_up'),
    url(r'^add_comment/(\d+)/$', 'core.views.add_comment', name='add_comment'),
    url(r'^user/(.*)/$', 'core.views.show_profile', name='show_profile'),
)
