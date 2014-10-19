import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.utils.text import slugify

from core.models import FinetoothUser, Post, Comment, Tag
from core.forms import CommentForm
from core.views.view_utils import (
    scored_context, paginated_view, paginated_context, tag_cloud_context
)


@paginated_view
def home(request, page_number):
    all_posts = Post.objects.all()
    context = paginated_context(request, 'posts', all_posts, page_number, {})
    context = scored_context(context['posts'], context)
    context['cloud'] = tag_cloud_context(Tag.objects.all())
    return render(request, "home.html", context)

@sensitive_post_parameters('password')
def sign_up(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            # TODO: require confirm_password as well; it would be sad
            # to be locked out of your new account because you
            # mistyped your intended password and didn't notice
            FinetoothUser.objects.create_user(username, email, password)
            messages.success(request, "Account creation successful!")
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return redirect("home")
        except IntegrityError:
            messages.error(request, "Username already exists.")
            return redirect("sign_up")
    else:
        return render(request, 'sign_up.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")

def show_post(request, year, month, slug):
    post = Post.objects.get(
        slug=slug, published_at__year=int(year), published_at__month=int(month)
    )
    top_level_comments = post.comment_set.filter(parent=None)
    return render(
        request, "post.html",
        scored_context([post], {'post': post, 'comment_form': CommentForm(),
                                'top_level_comments': top_level_comments})
    )

@login_required
def new_post(request):
    url = HttpRequest.build_absolute_uri(request, reverse("home"))
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        slug = request.POST["slug"]
        new_post = Post.objects.create(
            content=content, title=title, author=request.user,
            published_at=datetime.now(), slug=slug
        )
        return redirect(
            reverse(
                "show_post",
                args=(new_post.year, new_post.month, new_post.slug)
            )
        )
    else:
        return render(request, "new_post.html", {"url": url})

@paginated_view
def tagged(request, label, page_number):
    tag = Tag.objects.get(label=label)
    tagged_posts = tag.posts.all()
    context = paginated_context(
        request, 'posts', tagged_posts, page_number, {'tag': tag}
    )
    context = scored_context(context['posts'], context)
    return render(request, "tagged.html", context)

@login_required
@require_POST
def add_comment(request, post_pk):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(pk=post_pk)
    year_month_slug = (post.year, post.month, post.slug)
    if comment_form.is_valid():
        comment = Comment.objects.create(
            content=comment_form.cleaned_data['content'],
            commenter=request.user, post_id=post_pk,
            parent_id=request.POST.get('parent')
        )
        fragment_identifier = "#comment-{}".format(comment.pk)
        return redirect(
            reverse("show_post", args=year_month_slug) + fragment_identifier
        )
    else:
        messages.error(request, "Comments may not be blank.")
        return redirect('show_post', *year_month_slug)

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
            messages.success(request, "Profile editing successful!")
            return redirect('show_profile', the_user)
        else:
            return render(request, "edit_profile.html")
    else:
        return HttpResponseForbidden("You are not the user concerned!")
