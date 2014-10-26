from django.conf import settings

from core.models import Tag
from core.views.view_utils import tag_cloud_context

def tag_cloud_context_processor(request):
    return {'cloud': tag_cloud_context(Tag.objects.all())}

def contextual_static_serving_context_processor(request):
    if settings.SERVE_STATIC_LIBS_LOCALLY:
        jquery_url = "/static/libs/jquery-2.1.1.min.js"
        underscore_url = "/static/libs/underscore-min.js"
    else:
        jquery_url = "//code.jquery.com/jquery-2.1.1.min.js"
        underscore_url = "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min.js"
    return locals()
