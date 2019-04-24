from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
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
            return redirect('post-detail', pk=post.id)
        return None

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        text = ''
        with open('core/posts/'+str(pk)+'.html') as f:
            text = f.read()
        return render(request,
            'core/post_edit.html',
            context={'id': pk,
            'form': form,
            'text': text,})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            with open('core/posts/'+str(post.id)+'.html', 'w') as f:
                f.write(request.POST['text'])
            return redirect('post-detail', pk=post.id)