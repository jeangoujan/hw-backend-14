from django.test import TestCase
from .models import News, Comment
from datetime import datetime, timedelta
from django.urls import reverse
# Create your tests here.
class NewsModelTests(TestCase):
    def test_has_comments(self):
        news = News.objects.create(title="Test News True", content="Just for testing")
        Comment.objects.create(content="Test comment", news=news)
        self.assertTrue(news.has_comments())
    
    def test_has_not_comments(self):
        news = News.objects.create(title="Test News False", content="Just for testing")
        self.assertFalse(news.has_comments())
    

class NewsViewsTests(TestCase):
    def setUp(self):
        self.news1 = News.objects.create(title="Новость 1", content="Контент 1", created_at=datetime.now())
        self.news2 = News.objects.create(title="Новость 2", content="Контент 2", created_at=datetime.now() - timedelta(hours=10))
        self.news3 = News.objects.create(title="Новость 3", content="Контент 3", created_at=datetime.now() - timedelta(hours=15))

        self.comment1 = Comment.objects.create(content="Комментарий 1", news=self.news1, created_at=datetime.now())
        self.comment2 = Comment.objects.create(content="Комментарий 2", news=self.news1, created_at=datetime.now() - timedelta(minutes=10))
        self.comment3 = Comment.objects.create(content="Комментарий 3", news=self.news1, created_at=datetime.now() - timedelta(minutes=20))

    def test_news_sorted_desc(self):
        response = self.client.get(reverse("news_list"))
        self.assertEqual(response.status_code, 200)
    
        news_list = list(response.context["news_list"])
        expected_result = [self.news3, self.news2, self.news1]
        self.assertEqual(news_list, expected_result)
    
    def test_news_detail(self):
        response = self.client.get(reverse("news_detail", args=[self.news1.id])) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новость 1")  
        self.assertContains(response, "Контент 1") 

    def test_news_comments_sorted(self):
        response = self.client.get(reverse("news_detail", args=[self.news1.id]))  
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context)
        comments = response.context["comments"]
        self.assertEqual(comments[0], self.comment1) 
        self.assertEqual(comments[1], self.comment2)
        self.assertEqual(comments[2], self.comment3) 