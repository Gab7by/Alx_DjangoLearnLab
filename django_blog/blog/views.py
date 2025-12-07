from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, UpdateForm
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post
from .forms import PostForm

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
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10  # optional

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

