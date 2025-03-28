from django.urls import path
from .views import news_list, news_detail, add_news

urlpatterns = [
    path('', news_list, name='news_list'),
    path('<int:news_id>/', news_detail, name='news_detail'),
    path('add/', add_news, name='add_news'),
]
