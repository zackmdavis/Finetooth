from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login

from core import views, feeds

urlpatterns = patterns(
    '',
    url(r'^(?:page/(\d+)/)?$', views.home, name='home'),
    url(r'^valuation_(-?\d+)-([0-9a-f]{6})_(-?\d+)-([0-9a-f]{6}).css$',
        views.serve_stylesheet, name='stylesheet'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^tag/(\d+)/$', views.tag, name='tag'),
    url(r'^tagged/([-\w\s]*)/(?:page/(\d+)/)?$', views.tagged,
        name='tagged'),
    url(r'^vote/(?P<kind>.+)/(?P<pk>\d+)/$',
        views.ballot_box, name='vote'),
    url(r'^login/', login, {'template_name': "login.html"}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^user/(.+)/$', views.show_profile, name='show_profile'),
    url(r'^edit_profile/(.+)/$', views.edit_profile, name='edit_profile'),
    url(r'^add_comment/(\d+)/$', views.add_comment, name='add_comment'),
    url(r'^check_slug/$', views.check_slug, name='check_slug'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?:page/(?P<page>\d+)/)?$',
        views.MonthlyArchive.as_view(),
        name='monthly_archive'),
    url(r'^(\d{4})/(\d{2})/([a-z\d\-]+)/$', views.show_post, name='show_post'),

    url(r'feeds/rss/', feeds.LatestPostsFeed(), name='main_rss'),
)
