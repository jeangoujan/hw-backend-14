from django.contrib import admin
from .models import News, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5



# admin.site.register(News)
admin.site.register(Comment)

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    fields = ("title", "content", "created_at", "display_has_comments")
    readonly_fields = ("created_at",)
    inlines = [CommentInline]

    @admin.display(boolean=True, description="Есть комментарии")
    def display_has_comments(self, obj):
        return obj.has_comments()