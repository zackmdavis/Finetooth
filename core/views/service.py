from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseForbidden
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from core.models import Post, Comment, Tag
from core.colorize import stylesheet
from core.votable import VotingException


def serve_stylesheet(request, low_score, low_color, high_score, high_color):
    return HttpResponse(
        stylesheet(int(low_score), low_color, int(high_score), high_color),
        content_type="text/css"
    )

@login_required
@require_POST
def tag(request, post_slug):
    label = request.POST['label']
    post = Post.objects.get(slug=post_slug)
    if post.author != request.user:
        return HttpResponseForbidden("You can't tag other user's posts.")
    tag = Tag.objects.filter(label=label).first()
    if tag:
        if post.tag_set.filter(pk=tag.pk):
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
def ballot_box(request, kind, pk):
    if not request.user.is_authenticated():
        return HttpResponse("You must be logged in to vote!", status=401)
    kinds = {"post": Post, "comment": Comment}
    value = int(request.POST['value'])
    selection = request.POST['selection']
    item = kinds[kind].objects.get(pk=pk)
    try:
        item.accept_vote(request.user, selection, value)
        return HttpResponse(status=204)
    except VotingException as e:
        return HttpResponse(str(e), status=400)
