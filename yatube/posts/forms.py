from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']

        def clean_text(self):
            data = self.cleaned_data['text']
            return data

        def clean_group(self):
            data = self.cleaned_data['group']
            return data
