from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db import IntegrityError

from core.models import Post, Comment, FinetoothUser
from core.colorize import stylesheet
from core.forms import CommentForm

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
    comment_form = CommentForm()
    top_level_comments = post.comment_set.filter(parent=None)    
    return render(
        request, "post.html",
        {'post': post, 'comment_form': comment_form,
         'top_level_comments': top_level_comments,
         'low_score': low_score, 'high_score': high_score,
         'low_color': "ff0000", 'high_color': "0000ff"}
    )

@csrf_exempt
@login_required
@require_POST
def add_comment(request, pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        Comment.objects.create(
            content=comment_form.cleaned_data['content'],
            commenter=request.user, post_id=pk,
            parent_id=request.POST.get('parent')
        )
        return redirect(reverse("show_post", args=(pk,)))

def sign_up(request):
   if  request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = FinetoothUser.objects.create_user(username, email, password)
            return render(request, 'account_creation_successful.html', {})
        except IntegrityError:
            return render(request, 'duplicate_user.html')        
   else:
       return render(request, 'sign_up.html',)

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
        return HttpResponse(status=401)
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
