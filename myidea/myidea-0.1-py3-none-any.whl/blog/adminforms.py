from dal import autocomplete
from django import forms

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Post, Tag


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.TextInput(), label='desc', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        # widget=autocomplete.ModelSelect2(url='/category-autocomplete/'),
        label='category',
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        # widget=autocomplete.ModelSelect2Multiple(url='/tag-autocomplete/'),
        label='tag',
    )

    # content = forms.CharField(widget=CKEditorWidget(), label='content', required=False)
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='content', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='content', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), label='content', required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'is_md', 'content', 'content_md', 'content_ck',
            'status'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, 'mandatory field')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js',)



