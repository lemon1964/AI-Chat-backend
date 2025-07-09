# backend/chat_app/admin.py
from django.contrib import admin
from .models import Category, Question, Answer, GeneratedImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "owner")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("prompt", "category", "user", "model", "model_type", "created_at")
    search_fields = ("prompt", "category", "user")
    list_filter = ("model_type",)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("content", "question", "tokens_used")
    search_fields = ("content", "question", "tokens_used")


class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ("image", "prompt", "created_at")
    search_fields = ("image", "prompt", "created_at")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(GeneratedImage)
