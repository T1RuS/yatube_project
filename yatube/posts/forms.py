from django import forms
from .models import Group

GROUPS = tuple(Group.objects.values_list('title'))


class CreationPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
