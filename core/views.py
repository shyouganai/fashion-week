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


def post_create(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request,
            'core/post_create.html',
            context={'form': form,})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            with open('core/posts/'+str(post.id)+'.html', 'w') as f:
                f.write(request.POST['text'])
        return render(request,
            'index.html',)