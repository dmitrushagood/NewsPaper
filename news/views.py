from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Author
from datetime import datetime
from .search import Posts_filter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    template_name = 'news/Posts.html'
    context_object_name = 'Posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class Posts_search(ListView):
    model = Post
    template_name = 'news/Posts_search.html'
    context_object_name = 'Posts_search'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = Posts_filter(self.request.GET,
                                         queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


class PostCreate(PermissionRequiredMixin, CreateView):  # Ограничение прав доступа
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_Post',
                           'news.change_Post')


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # Ограничение прав доступа
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_Post',
                           'news.change_Post')


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'news/post_delete.html'

    queryset = Post.objects.all()
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    p = request.user.id
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user_id=p)
    return redirect('/news')
