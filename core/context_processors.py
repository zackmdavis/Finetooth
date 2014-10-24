from core.models import Tag
from core.views.view_utils import tag_cloud_context

def tag_cloud_context_processor(request):
    return {'cloud': tag_cloud_context(Tag.objects.all())}
