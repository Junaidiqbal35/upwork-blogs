from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Post
from ckeditor.fields import RichTextField


class PostForm(forms.ModelForm):

    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('category', 'title', 'body', 'image', 'status')


class SearchForm(forms.Form):
    q = forms.CharField(max_length=255)
