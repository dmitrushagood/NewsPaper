from django.shortcuts import render

from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том, что
# в этом представлении мы будем выводить список объектов из БД
from .models import Post
from datetime import datetime


class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'Posts.html'  # указываем имя шаблона, где будет лежать HTML, в котором будут все
    # инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'Posts'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'Post'
