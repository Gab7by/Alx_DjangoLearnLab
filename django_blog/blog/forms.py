from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag
from .models import Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit: 
            user.save()
        return user
    
class UpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email"]

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. django, python, tips)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # author & published_date set automatically
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post...', 'class': 'form-control', 'rows': 8}),
        }
        
    def __init__(self, *args, **kwargs):
        # if editing, populate tags field with existing tags
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        # split, strip, remove empties, lower-case unique
        names = []
        for part in raw.split(','):
            name = part.strip()
            if name:
                names.append(name)
        # remove duplicates while preserving order
        seen = set(); uniq = []
        for n in names:
            if n.lower() not in seen:
                uniq.append(n)
                seen.add(n.lower())
        return uniq  # list of tag names

    def save(self, commit=True):
        tags = self.cleaned_data.pop('tags', [])
        post = super().save(commit=commit)
        # attach tags after saving post
        # create tag objects if they don't exist
        tag_objs = []
        for name in tags:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)
        # replace M2M relation
        post.tags.set(tag_objs)
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        label='',
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment is too long (max 2000 characters).")
        return content