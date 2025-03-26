from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import News
from django.utils.timezone import now
from django.views import View
from .forms import NewsForm, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
# Create your views here.
def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news})

from .models import Comment

@login_required
def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = Comment.objects.filter(news=news).order_by("-created_at")

    can_delete_news = request.user == news.author or request.user.has_perm("news.delete_news")
    def can_delete_comment(comment):
        return request.user == comment.author or request.user.has_perm("news.delete_comment")

    if request.method == "POST":
        if request.user.has_perm("news.add_comment"):
            content = request.POST.get("content")
            if content:
                Comment.objects.create(news=news, content=content, author=request.user)
                return redirect("news_detail", news_id=news.id)
        else:
            return HttpResponseForbidden("У вас нет прав для добавления комментариев")

    return render(request, "news/news_detail.html", {
        "news": news,
        "comments": comments,
        "can_delete_news": can_delete_news,
        "can_delete_comment": can_delete_comment,
    })


 
@login_required
@permission_required('news.add_news', raise_exception=True)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.created_at = now()
            news.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'news.can_edit_news'
    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        if request.user != news.author and not request.user.has_perm("news.can_edit_news"):
            return redirect('news_detail', news_id=news.id)

        form = NewsForm(instance=news)
        return render(request, 'news/edit_news.html', {'form': form, 'news': news})

    def post(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        if request.user != news.author and not request.user.has_perm("news.can_edit_news"):
            return redirect('news_detail', news_id=news.id)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', news_id=news.id)

        return render(request, 'news/edit_news.html', {'form': form, 'news': news})

    

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_group, created = Group.objects.get_or_create(name='default')
            user.groups.add(default_group) 
            return redirect('login')
        return render(request, 'registration/sign_up.html', {'form': form})
    

@login_required
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.user == news.author or request.user.has_perm("news.delete_news"):
        news.delete()
        return redirect("news_list")

    raise PermissionDenied
    
@login_required
@permission_required('news.can_delete_comment', raise_exception=True)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        return redirect('news_detail', news_id=comment.news.id)
    else:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий")