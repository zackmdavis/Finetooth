import calendar
from collections import Counter

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from core.models import Post, Tag
from core.views.view_utils import tag_cloud_context

def tag_cloud_context_processor(request):
    return {'cloud': tag_cloud_context(Tag.objects.all())}

def sidebar_login_form_context_processor(request):
    return {'sidebar_login_form': AuthenticationForm() }

def monthly_archives_context_processor(request):
    month_counts = Counter([(p.year, p.month)
                            for p in Post.objects.all()])
    month_counts = sorted(
        month_counts.items(),
        key=lambda k: (int(k[0][0]), int(k[0][1]))
    )
    months_info = [
        (
            archive[0],
            "{} {} ({})".format(
                calendar.month_name[int(archive[0][1])], archive[0][0],
                archive[1]
            )
        ) for archive in month_counts
    ]
    return {'months': months_info}

def contextual_static_serving_context_processor(request):
    if settings.SERVE_STATIC_LIBS_LOCALLY:
        jquery_url = "/static/libs/jquery-2.1.1.min.js"
        underscore_url = "/static/libs/underscore-min.js"
    else:
        jquery_url = "//code.jquery.com/jquery-2.1.1.min.js"
        underscore_url = ("//cdnjs.cloudflare.com/ajax/libs/underscore.js/"
                          "1.7.0/underscore-min.js")
    return locals()
