from datetime import datetime
import calendar

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpRequest
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.template.response import TemplateResponse
from django.utils.text import slugify
from django.utils.translation import ugettext as _

import bleach

from core.models import FinetoothUser, Post, Comment, Tag
from core.forms import CommentForm, SignupForm
from core.views.view_utils import (
    score_bound_context_supplement, scored_view,
    paginated_view, thread_sorting_view
)


@paginated_view('posts')
@scored_view('posts')
def home(request, page_number=None):
    all_posts = Post.objects.all() \
                            .prefetch_related('vote_set') \
                            .prefetch_related('comment_set') \
                            .select_related('author')
    for post in all_posts:
        post.request_user = request.user
    return TemplateResponse(request, "home.html", {'posts': all_posts})


@sensitive_post_parameters('password', 'confirm_password')
def sign_up(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data["username"]
            email = signup_form.cleaned_data["email"]
            password = signup_form.cleaned_data["password"]
            FinetoothUser.objects.create_user(username, email, password)
            messages.success(request, _("Account creation successful!"))
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect("home")
        else:
            messages.warning(request, signup_form.errors)
            return render(
                request, 'sign_up.html', {'signup_form': signup_form},
                status=422
            )
    else:
        signup_form = SignupForm()
        return render(request, 'sign_up.html', {'signup_form': signup_form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")


@thread_sorting_view
@scored_view('posts')
def show_post(request, year, month, slug):
    post = Post.objects.get(
        slug=slug, published_at__year=int(year), published_at__month=int(month)
    )
    post.request_user = request.user
    top_level_comments = post.comment_set.filter(parent=None)
    return TemplateResponse(
        request, "post.html",
        {'post': post,
         'posts': [post],  # XXX awkward
         'comment_form': CommentForm(),
         'top_level_comments': top_level_comments}
    )


class MonthlyArchive(ListView):
    context_object_name = 'posts'
    template_name = 'monthly_archive.html'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        start_of_month = datetime(year=year, month=month, day=1)
        end_year = year if month < 12 else (year + 1)
        next_month = (month % 12) + 1
        end_of_month = datetime(year=end_year, month=next_month, day=1)
        # XXX: is it possible to use my post.request_user hack with
        # class-based views??
        return Post.objects.filter(
            published_at__gte=start_of_month, published_at__lt=end_of_month
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = int(self.kwargs['year'])
        context['month'] = _(calendar.month_name[int(self.kwargs['month'])])
        return context

@login_required
def new_post(request):
    url = HttpRequest.build_absolute_uri(request, reverse("home"))
    if request.method == "POST":
        content = bleach.clean(request.POST["content"])
        title = request.POST["title"]
        slug = request.POST["slug"]
        new_post = Post(
            content=content, title=title, author=request.user,
            published_at=datetime.now(), slug=slug
        )
        try:
            new_post.full_clean()
        # XXX: we really should just be using a ModelForm
        except ValidationError as e:
            # XXX: this way of rendering the error message ends up
            # looking too JSONy from a user's perspective
            messages.error(request, str(e))
            return redirect(reverse('new_post'))
        new_post.save()
        return redirect(
            reverse(
                "show_post",
                args=(new_post.year, new_post.month, new_post.slug)
            )
        )
    else:
        return render(request, "new_post.html", {"url": url})

@paginated_view('posts')
@scored_view('posts')
def tagged(request, label, page_number=None):
    tag = Tag.objects.get(label=label)
    tagged_posts = tag.posts.all()
    for post in tagged_posts:
        post.request_user = request.user
    return TemplateResponse(request, "tagged.html",
                            {'tag': tag, 'posts': tagged_posts})

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
        messages.warning(request, "Comments may not be blank.")
        return redirect('show_post', *year_month_slug)

def show_profile(request, username):
    the_user = FinetoothUser.objects.filter(username=username).first()
    if the_user is None:
        messages.error(request, "That user does not exist.")
        return redirect('home')
    viewing_user = request.user
    posts = Post.objects.filter(author=the_user).prefetch_related(
        'comment_set').prefetch_related('vote_set')
    comments = Comment.objects.filter(commenter=the_user)
    return render(request, "profile.html",
                  {'the_user': the_user,
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
            messages.success(request, _("Profile editing successful!"))
            return redirect('show_profile', the_user)
        else:
            return render(request, "edit_profile.html")
    else:
        return HttpResponseForbidden(_("You are not the user concerned!"))
