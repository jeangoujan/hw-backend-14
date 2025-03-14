from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News
from django.utils.timezone import now

# Create your views here.
def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})

from .models import Comment

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = news.comments.all()

    if request.method == "POST":
        content = request.POST.get('content')
        Comment.objects.create(news=news, content=content)
        return redirect('news_detail', news_id=news.id)

    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments})


def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content, created_at=now())
        return redirect('news_detail', news_id=news.id)
    return render(request, 'news/add_news.html')