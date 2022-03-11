from django.urls import path
from .views import PostsList, PostDetail, Posts_search, PostCreate,  PostDelete, PostUpdate, IndexView
from .views import upgrade_me

urlpatterns = [
    path('news/', PostsList.as_view()),
    #path('', PostsList.as_view()), не удалил на случай изменений в будущем
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', Posts_search.as_view(), name='Posts_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    ]