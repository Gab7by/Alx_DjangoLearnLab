from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, UpdateForm
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.db.models import Q

def register(request):
    if request.method == "POST":
       form = RegisterForm(request.POST)
       if form.Is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request, f"Account created for {username}. You can now log in.") 
           return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your profile was updated.")
            return redirect('profile')
    else:
        u_form = UpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'blog/profile.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # templates/blog/post_list.html
    context_object_name = 'post'
    ordering = ['-published_date']
    paginate_by = 10  # optional
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        # comments available as post.comments.all() via related_name
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # templates/blog/post_detail.html
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # where to redirect after successful creation
    def form_valid(self, form):
        # set the post author to the logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # ensure author stays unchanged
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user  # only author may update

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user 

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # fallback template if you visit direct
    # We will pass post_pk via URL

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object().post.pk})

class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        # search title OR content OR tag name (case-insensitive)
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        ctx['tag_name'] = tag_name
        return ctx

class TagListView(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
