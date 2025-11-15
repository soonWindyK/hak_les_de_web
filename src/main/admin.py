from django.contrib import admin
from .models import NKO, News, Event, KnowledgeItem, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'patronymic', 'city', 'phone']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'patronymic']


@admin.register(NKO)
class NKOAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'is_approved', 'created_at']
    list_filter = ['category', 'city', 'is_approved']
    search_fields = ['name', 'description']
    list_editable = ['is_approved']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'author', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'city', 'organizer', 'is_approved', 'created_at']
    list_filter = ['category', 'city', 'is_approved', 'date']
    search_fields = ['title', 'description']
    list_editable = ['is_approved']


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'created_by', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title', 'description']
