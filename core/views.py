from datetime import datetime

from django.shortcuts import render, redirect
from django.http import (
<<<<<<< HEAD
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
=======
    HttpResponse, HttpResponseRedirect, HttpResponseForbidden
>>>>>>> e053d910341b513a60ed6ae94feeb1c4f65fd260
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError

from core.models import FinetoothUser, Post, Comment, Tag
from core.colorize import stylesheet
from core.forms import CommentForm
from core.votable import VotingException


def home(request):
    posts = Post.objects.all()
    if posts:
        low_score = min(p.low_score() for p in posts)
        high_score = max(p.high_score() for p in posts)
    else:
        low_score, high_score = 0, 0
    return render(
        request, "home.html",
        {'posts': posts,
         'low_score': low_score, 'high_score': high_score,
         'low_color': "ff0000", 'high_color': "0000ff"}
    )

def serve_stylesheet(request, low_score, low_color, high_score, high_color):
    return HttpResponse(
        stylesheet(int(low_score), low_color, int(high_score), high_color),
        content_type="text/css"
    )

def logout_view(request):
    logout(request)
    return redirect("/")

def show_post(request, pk):
    # TODO: looking up posts by ID number is super ugly; we probably
    # want to store URL slugs in the post model (and index that
    # column!) and look them up that way?
    post = Post.objects.get(pk=pk)
    if post:
        low_score = post.low_score()
        high_score = post.high_score()
    else:
        low_score, high_score = 0, 0
    top_level_comments = post.comment_set.filter(parent=None)
    return render(
        request, "post.html",
        {'post': post, 'comment_form': CommentForm(),
         'top_level_comments': top_level_comments,
         'low_score': low_score, 'high_score': high_score,
         'low_color': "ff0000", 'high_color': "0000ff"}
    )

def tagged(request, label):
    tag = Tag.objects.get(label=label)
    posts = tag.posts.all()
    if posts:  # XXX TODO FIXME: ugly code duplication; maybe can pull
        low_score = min(p.low_score() for p in posts)  # into decorator?
        high_score = max(p.high_score() for p in posts)
    else:
        low_score, high_score = 0, 0
    return render(request, "tagged.html",
                  {'tag': tag, 'posts': posts,
                   'low_score': low_score, 'high_score': high_score,
                   'low_color': "ff0000", 'high_color': "0000ff"})

@csrf_exempt
@login_required
@require_POST
def add_comment(request, post_pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = Comment.objects.create(
            content=comment_form.cleaned_data['content'],
            commenter=request.user, post_id=post_pk,
            parent_id=request.POST.get('parent')
        )
        fragment_identifier = "#comment-{}".format(comment.pk)
        return redirect(
            reverse("show_post", args=(post_pk,)) + fragment_identifier
        )
    else:
        messages.error(request, "Comments may not be blank.")
        return redirect('show_post', post_pk)

def sign_up(request):
   if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = FinetoothUser.objects.create_user(username, email, password)
            return render(request, 'account_creation_successful.html')
        except IntegrityError:
            return render(request, 'duplicate_user.html')
   else:
       return render(request, 'sign_up.html')

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        new_post = Post.objects.create(
            content=content, title=title, author=request.user,
            published_at=datetime.now()
        )
        return redirect(reverse("show_post", args=(new_post.pk,)))
    else:
        return render(request, "new_post.html", {})

@login_required
@require_POST
@csrf_exempt
def tag(request, post_pk):
    label = request.POST['label']
    post = Post.objects.get(pk=post_pk)
    if post.author != request.user:
        return HttpResponseForbidden("You can't tag other user's posts.")
    tag = Tag.objects.filter(label=label).first()
    if tag:
        if post.tag_set.filter(pk=tag.pk):
            return HttpResponse(
                "This post is already tagged {}".format(label), status=400
            )
        else:
            post.tag_set.add(tag)
            return HttpResponse(status=204)
    else:
        post.tag_set.create(label=label)
        return HttpResponse(status=204)

@require_POST
@csrf_exempt
def ballot_box(request, kind, pk):
    if not request.user.is_authenticated():
        return HttpResponse(status=401)
    kinds = {"post": Post, "comment": Comment}
    value = int(request.POST['value'])
    selection = request.POST['selection']
    item = kinds[kind].objects.get(pk=pk)
    try:
        item.accept_vote(request.user, selection, value)
        return HttpResponse(status=204)
    except VotingException:
        return HttpResponse(status=400)

def show_profile(request, username):
    the_user = FinetoothUser.objects.get(username=username)
    viewing_user = request.user
    posts = Post.objects.filter(author=the_user)
    comments = Comment.objects.filter(commenter=the_user)
    return render(request, "profile.html",
                  {'the_user': the_user,
                   'viewing_user': viewing_user,
                   'posts': posts, 'comments': comments})

def edit_profile(request, username):
    the_user = FinetoothUser.objects.get(username=username)
    if the_user == request.user:
        if request.method == "POST":
            url = request.POST["url"]
            location = request.POST["location"]
            if url:
                the_user.url = url
            if location:
                the_user.location = location
            the_user.save()
            return redirect("profile_success")
        else:
            return render(request, "edit_profile.html")
    else:
        return HttpResponseForbidden("You are not the user concerned!")

def profile_success(request):
    return render(request, "profile_success.html")
