from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

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
    class Meta:
        model = Post
        fields = ['title', 'content']  # author & published_date set automatically
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post...', 'class': 'form-control', 'rows': 8}),
        }