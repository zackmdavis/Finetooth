from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.models import Post, Comment

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {'posts': posts})

def show_post(request, pk):
    # TODO: looking up posts by ID number is super ugly; we probably
    # want to store URL slugs in the post model (and index that
    # column!) and look them up that way?
    post = Post.objects.get(pk=pk)
    return render(request, "post.html", {'post': post})

@require_POST
@csrf_exempt
def ballot_box(request, kind, pk, value):
    kinds = {"post": Post, "comment": Comment}
    kinds[kind].objects.get(pk=pk).vote_set.create(
        value=value,
        # arbitrary values to prevent IntegrityErrors until I get
        # around to fixing this
        start_index=0, end_index=2
    )
    return HttpResponse(status=204)
