import re
from functools import wraps
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

def scored_context(scoreables, context):
    if scoreables:
        low_score = min(s.low_score() for s in scoreables)
        high_score = max(s.high_score() for s in scoreables)
    else:
        low_score, high_score = 0, 0
    context.update({
        'low_score': low_score, 'high_score': high_score,
        'low_color': "ff0000", 'high_color': "0000ff"
    })
    return context

class PaginationRedirection(Exception):
    def __init__(self, response):
        super().__init__()
        self.response = response

def paginated_view(view):
    @wraps(view)
    def pagination_redirection_wrapper(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except PaginationRedirection as pr:
            return pr.response
    return pagination_redirection_wrapper

def paginated_context(request, pageable_name, pageables, page_number, context):
    page_number = int(page_number) if page_number else 1
    requested = request.GET.get('results')
    pageables_per_page = (int(requested) if (requested and requested.isdigit())
                          else settings.POSTS_PER_PAGE)
    paginator = Paginator(pageables, pageables_per_page)
    if page_number > paginator.num_pages:
        true_destination = re.sub(
            r'/page/(\d+)/',
            ''.join([
                "/page/{}/".format(paginator.num_pages),
                "?", urlencode(request.GET)
            ]),
            request.path
        )
        messages.warning(
            request, ("The page you requested is out of range; "
                      "you have been redirected to the last page.")
        )
        raise PaginationRedirection(HttpResponseRedirect(true_destination))
    paged = paginator.page(page_number)
    context.update({
        pageable_name: paged,
        'previous_page_number': (page_number - 1 if paged.has_previous()
                                 else None),
        'next_page_number': (page_number + 1 if paged.has_next()
                             else None),
        'requested': requested
    })
    return context
