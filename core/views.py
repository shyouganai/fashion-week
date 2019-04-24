from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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

def post_create(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PostForm()
            return render(request,
                'core/post_create.html',
                context={'form': form,})
        else:
            return redirect('index')
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

class PostCreateView(generic.base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = PostForm()
            return render(request,
                'core/post_create.html',
                context={'form': form,})
        else:
            return redirect('index')

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            with open('core/posts/'+str(post.id)+'.html', 'w') as f:
                f.write(request.POST['text'])
            return redirect('post-detail', pk=post.id)
        return None

class PostEditView(generic.base.View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = PostForm(instance=post)
        text = ''
        with open('core/posts/'+str(post.id)+'.html') as f:
            text = f.read()
        return render(request,
            'core/post_edit.html',
            context={'id': post.id,
            'form': form,
            'text': text,})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            with open('core/posts/'+str(post.id)+'.html', 'w') as f:
                f.write(request.POST['text'])
            return redirect('post-detail', pk=post.id)

class PostDeleteView(generic.base.View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user.is_authenticated and post.author == request.user:
            post.delete()
        return redirect('index')


class CommentListView(generic.ListView):
    model = Comment


# Accounts
class LoginFormView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class RegisterFormView(generic.FormView):
    form_class = UserCreationForm
    template_name = 'registration.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LogoutView(generic.base.View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')