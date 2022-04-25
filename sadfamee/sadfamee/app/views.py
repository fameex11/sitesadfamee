from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import *
from .models import Blog
from django.template import loader
from .models import Comment
from .forms import CommentForm
from django.views.generic import UpdateView
from .forms import BlogForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'',
            'year':datetime.now().year,
        }
    )


def brif(request):
    assert isinstance(request, HttpRequest)
    data = None
    genders ={
               '1': 'Мужской',
               '2': 'Женский'
             }
    form = Brif(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = genders[form.cleaned_data['gender']]
            data['message'] = form.cleaned_data['message']
            if (form.cleaned_data['answer'] == True):
                data['answer'] = 'Да'
            else:
                data['answer'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form=Brif()
    return render(request, 'app/brif.html',
                {
                    'form': form,
                    'data': data
                })


def registr(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return render(request, 'app/about.html')
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(request, 'app/registr.html',
    {
    'regform': regform, # передача формы в шаблон веб-страницы
    'year':datetime.now().year,
    }
    )

def blogs(request):
    lastblogs=Blog.objects.order_by('-posted')[:10]
    template = loader.get_template('app/blogs.html')
    context = {
    'lastblogs': lastblogs,
}
    return render(request, 'app/blogs.html',context)


def detals(request, Blog_id):
    comments = Comment.objects.order_by('-posted')
    blog = Blog.objects.get(pk=Blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.posted = datetime.now()
            comment_f.post = Blog.objects.get(pk=Blog_id)
            comment_f.save()
            return render(request, 'app/detals.html', {'blog': blog,
                                    'comments': comments,
                                    'form': form
                                    })
    form = CommentForm()
    return render(request, 'app/detals.html', {'blog': blog,
                                'comments': comments,
                                'form': form
                                 })

def videos(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videos.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )
class Redakt(UpdateView):
    model = Blog
    pk_url_kwarg = "Blog_id"
    template_name = 'app/redakt.html'
    form_class = BlogForm

def create(request):
    error = ''
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            u_add = form.save(commit=False)
            u_add.author = request.user
            u_add.posted = datetime.now()
            form.save()
            return render(request, 'app/blogs.html')
        else:
            error = 'Форма заполнена некорректно'
    form = BlogForm()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'app/create.html', data)