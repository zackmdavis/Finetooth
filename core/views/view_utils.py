import re
from functools import wraps
from urllib.parse import urlencode

from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings


def score_bound_context_supplement(scorables):
    if scorables:
        low_score = min(s.low_score() for s in scorables)
        high_score = max(s.high_score() for s in scorables)
    else:
        low_score, high_score = 0, 0
    return {
        # leave room on the scale for instarendering
        'low_score': low_score - 1, 'high_score': high_score + 1,
        'low_color': "ff0000", 'high_color': "0000ff"
    }

def scored_view(scorable_key):
    def derived_decorator(view):
        @wraps(view)
        def derived_view(*args, **kwargs):
            response = view(*args, **kwargs)
            response.context_data.update(
                score_bound_context_supplement(
                    response.context_data[scorable_key])
            )
            return response
        return derived_view
    return derived_decorator


def paginated_view(pageable_name):
    def derived_decorator(view):
        @wraps(view)
        def derived_view(*args, **kwargs):
            request, *_groups = args
            page_number = kwargs['page_number']
            response = view(*args, **kwargs)
            page_number = int(page_number) if page_number else 1
            requested = request.GET.get('results')
            pageables_per_page = (int(requested)
                                  if (requested and requested.isdigit())
                                  else settings.POSTS_PER_PAGE)
            pageables = response.context_data[pageable_name]
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
                return HttpResponseRedirect(true_destination)
            paged = paginator.page(page_number)
            response.context_data.update(
                {pageable_name: paged,
                 'previous_page_number': (page_number - 1
                                          if paged.has_previous()
                                          else None),
                 'next_page_number': (page_number + 1
                                      if paged.has_next()
                                      else None),
                 'requested': requested}
            )
            return response
        return derived_view
    return derived_decorator


def tag_cloud_context(tags):
    if not tags.exists():
        return {}
    min_size = 9
    max_size = 20
    tags = tags.annotate(Count('posts')).order_by('posts__count')
    min_count = tags[0].posts__count
    max_count = tags[tags.count()-1].posts__count
    def font_size(count):
        if max_count == min_count:
            return (max_size + min_size) / 2
        else:
            slope = (max_size - min_size) / (max_count - min_count)
            return min_size + slope * count
    return {tag: font_size(tag.posts__count) for tag in tags}
