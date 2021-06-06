from django.forms import ModelForm, TextInput, Textarea
from .models import Comment, Reply

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'コメント内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '返信内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }

# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

class SomeForm(forms.Form):
    foo = SummernoteTextFormField()

class FormForSomeModel(forms.ModelForm):
    foo = SummernoteTextField() 
