from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from core.models import Post, Comment

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {'posts': posts})

def logout_view(request):
    logout(request)
    return redirect("/")

def show_post(request, pk):
    # TODO: looking up posts by ID number is super ugly; we probably
    # want to store URL slugs in the post model (and index that
    # column!) and look them up that way?
    post = Post.objects.get(pk=pk)
    return render(request, "post.html", {'post': post})

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        new_post = Post.objects.create(
            content=content, title=title, author=request.user
        )
        return redirect(reverse("show_post", args=(new_post.pk,)))
    else:
        return render(request, "new_post.html", {})


@require_POST
@csrf_exempt
def ballot_box(request, kind, pk):
    if not request.user.is_authenticated():
        return HttpResponse(status=403)
    kinds = {"post": Post, "comment": Comment}
    value = int(request.POST['value'])
    selection = request.POST['selection']
    item = kinds[kind].objects.get(pk=pk)
    content = item.content
    # XXX what about when the selection appears more than once?
    start_index = content.find(selection)
    if start_index != -1:
        end_index = start_index + len(selection)
        item.vote_set.create(
            voter=request.user, value=value,
            start_index=start_index, end_index=end_index
        )
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)
