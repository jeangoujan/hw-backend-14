from django.urls import path
from .views import news_list, news_detail, add_news, NewsUpdateView, SignUpView, delete_news, delete_comment
from . import views

urlpatterns = [
    path('', news_list, name='news_list'),
    path('<int:news_id>/', news_detail, name='news_detail'),
    path('add/', add_news, name='add_news'),
    path('<int:news_id>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('<int:news_id>/delete/', delete_news, name='news_delete'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='comment_delete'),
]
