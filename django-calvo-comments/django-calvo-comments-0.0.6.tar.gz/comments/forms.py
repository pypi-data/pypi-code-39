from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from .models import Post, CommentPost

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', )
    def clean_content(self):
        data = self.cleaned_data.get('content')
        if len(data) <= 10:
            raise forms.ValidationError('Please enter at least 10 characters')
        return data

class CommentPostForm(forms.ModelForm):
    
    class Meta:
        model = CommentPost
        fields = ('title', 'text',)