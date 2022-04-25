"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import Blog
from .models import Comment
from django.forms import ModelForm, TextInput, Textarea

genders = [
    ('1', 'Мужской'),
    ('2', 'Женский')
]

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class Brif(forms.Form):
    name = forms.CharField(max_length=100, label='',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваше имя'
                            }))
    city = forms.CharField(max_length=100, label='',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваш город'
                            }))
    gender = forms.ChoiceField(label='Ваш пол',
                                choices = genders,
                                widget=forms.RadioSelect, initial=2)
    message = forms.CharField(label='',
                                widget=forms.Textarea(attrs={
                                    'rows': 5,
                                    'cols': 5,
                                    'class': 'form-control',
                                    'placeholder': 'Напишите отзыв о нашем сайте'
                                }))
    answer = forms.BooleanField(label='Отправить ответ вам', initial=True, required=False)
    email = forms.EmailField(max_length=100, label='',
                                widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Ваш e-mail'
                                }))

    class UserCreationForm(UserCreationForm):
        def _init_(self, args, **kwargs):
            super(UserCreationForm, self).init(args, **kwargs)
            self.fields['username'].help_text = ''
            self.fields['username'].label = 'Имя пользователя'
            self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
            self.fields['password1'].help_text = ''
            self.fields['password1'].label = 'Пароль'
            self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
            self.fields['password2'].help_text = ''
            self.fields['password2'].label = 'Повторите пароль'
            self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text = ''
        self.fields['text'].label = ''
        self.fields['text'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите текст комментария'})

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','description','content','image']

