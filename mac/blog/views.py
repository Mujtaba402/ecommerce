from django.shortcuts import render
from .models import BlogPost
from django.http import HttpResponse


# Create your views here.
def index(request):
    mypost = BlogPost.objects.all()
    return render(request, 'blog/index.html', {'mypost': mypost})


def blogpost(request, id):
    post = BlogPost.objects.filter(post_id=id)[0]

    return render(request, 'blog/blogpost.html', {'post': post})
