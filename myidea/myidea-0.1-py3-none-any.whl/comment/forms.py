from django import forms
import mistune

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='nickname',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width:60%;'}
        )
    )
    email = forms.CharField(
        label='email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width:60%;'}
        )
    )
    website = forms.CharField(
        label='website',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width:60%;'}
        )
    )
    content = forms.CharField(
        label='content',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('too short content, it should be longer than 10 chars')
        content = mistune.markdown(content, False)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
