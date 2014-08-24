from django.shortcuts import render

from core.models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {'posts': posts})

def show_post(request, pk):
    # TODO: looking up posts by ID number is super ugly; we probably
    # want to store URL slugs in the post model (and index that
    # column!) and look them up that way?
    post = Post.objects.get(pk=pk)
    return render(request, "post.html", {'post': post})
