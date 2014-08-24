from django.shortcuts import render

from core.models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", locals())
