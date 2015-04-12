import calendar
from collections import Counter

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _

from core.models import Post, Tag
from core.views.view_utils import tag_cloud_context


def tag_cloud_context_processor(request):
    return {'cloud': tag_cloud_context(Tag.objects.all())}

def sidebar_login_form_context_processor(request):
    return {'sidebar_login_form': AuthenticationForm()}

def monthly_archives_context_processor(request):
    month_counts = Counter([(p.year, p.month)
                            for p in Post.objects.all()])
    month_counts = sorted(
        month_counts.items(),
        key=lambda k: (int(k[0][0]), int(k[0][1]))
    )
    month_display_texts = [
        (
            month,
            "{month} {year} ({count})".format(
                month=_(calendar.month_name[int(month[1])]),
                year=month[0],
                count=count
            )
        ) for month, count in month_counts
    ]
    return {'months': month_display_texts}

def contextual_static_serving_context_processor(request):
    if settings.SERVE_STATIC_LIBS_LOCALLY:
        jquery_url = "/static/libs/jquery-2.1.1.min.js"
        underscore_url = "/static/libs/underscore-min.js"
        bootstrap_url = "/static/libs/css/bootstrap.min.css"
    else:
        jquery_url = "//code.jquery.com/jquery-2.1.1.min.js"
        underscore_url = ("//cdnjs.cloudflare.com/ajax/libs/underscore.js/"
                          "1.7.0/underscore-min.js")
        bootstrap_url = ("//netdna.bootstrapcdn.com/bootstrap/3.2.0/"
                         "css/bootstrap.min.css")
    return locals()
