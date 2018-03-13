from django import forms
from django.shortcuts import redirect
from .models import Post, Msg

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class MessageForm(forms.Form):
    user = forms.CharField(label='User id', max_length=100)
    message = forms.CharField(label='Message', max_length=200)

class NaviForm(forms.Form):
    page = forms.IntegerField(min_value=1, max_value=50)
