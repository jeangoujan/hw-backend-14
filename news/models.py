from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_edit_news", "Может редактировать новости"),
            ("can_delete_news", "Может удалять новости"),
        ]

    def __str__(self):
        return self.title
    
    def has_comments(self):
        return self.comments.exists()

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_delete_comment", "Может удалять комментарии"),
            ("can_add_comment", "Может добавлять комментарии"),
        ]

    def __str__(self):
        return f"Комментарий к {self.news.title}"

