from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import PostForm, CommentForm

def index(request):
    if request.method == 'GET':
    	posts = Post.objects.all().order_by('-datetime')
    	return render(request,
    		'index.html',
    		context={'posts': posts,})

class PostListView(generic.ListView):
    model = Post
    paginator_by = 10

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	context['text'] = ''
    	with open('core/posts/'+str(self.object.id)+'.html') as f:
    		context['text'] += f.read()
    	return context

class CommentListView(generic.ListView):
    model = Comment
