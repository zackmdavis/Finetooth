import json

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseForbidden, JsonResponse
)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from core.models import Post, Comment, Tag
from core.colorize import stylesheet

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


def serve_stylesheet(request, low_score, low_color, high_score, high_color):
    return HttpResponse(
        stylesheet(int(low_score), low_color, int(high_score), high_color),
        content_type="text/css"
    )

@login_required
@require_POST
def tag(request: WSGIRequest, post_pk: str) -> HttpResponse:
    label = request.POST['label']
    post = Post.objects.get(pk=post_pk)
    if post.author != request.user:
        return HttpResponseForbidden("You can't tag other user's posts.")
    tag = Tag.objects.filter(label=label).first()
    if tag:
        if post.tag_set.filter(pk=tag.pk).exists():
            return HttpResponseBadRequest(
                "This post is already tagged {}".format(label)
            )
        else:
            post.tag_set.add(tag)
            return HttpResponse(status=204)
    else:
        post.tag_set.create(label=label)
        return HttpResponse(status=204)

@require_POST
def ballot_box(request: WSGIRequest, kind: str, pk: str) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to vote!", status=401)
    kinds = {"post": Post, "comment": Comment}
    value = request.POST.get('value')
    start_index = int(request.POST.get('startIndex'))
    end_index = int(request.POST.get('endIndex'))
    item = kinds[kind].objects.get(pk=pk)
    if start_index < 0 or end_index > len(item.plaintext):
        return HttpResponseBadRequest("Invalid vote not recorded!")
    if item.vote_in_range_for_user(request.user, start_index, end_index):
        return HttpResponseForbidden("Overlapping votes are not allowed!")
    else:
        item.vote_set.create(
            voter=request.user, value=value,
            start_index=start_index, end_index=end_index
        )
        return HttpResponse(status=204)

def check_slug(request):
    slug = request.GET.get('slug')
    if slug is None:
        return HttpResponseBadRequest()
    already_exists = Post.objects.filter(slug=slug).exists()
    return JsonResponse({'alreadyExists': already_exists})
