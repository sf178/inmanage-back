from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.db import models
from django.forms import TextInput, DateInput
from datetime import datetime

from .models import *


class TodoItemInline(admin.TabularInline):
    model = TodoItem
    extra = 0


class TodoTaskAdmin(admin.ModelAdmin):
    inlines = [TodoItemInline]
    list_display = ('title', 'date_end')
    search_fields = ('title', 'date_end')
    list_filter = (('date_end', admin.DateFieldListFilter),)
    formfield_overrides = {
        models.DateField: {'widget': AdminDateWidget},
    }

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        try:
            date = search_term.split(' ')[0]
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            queryset |= self.model.objects.filter(due_date=date_obj)
        except (IndexError, ValueError):
            pass

        return queryset, use_distinct


class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'done')
    search_fields = ('id', 'done')
    list_filter = (('id', 'done'))

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        try:
            date = search_term.split(' ')[0]
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            queryset |= self.model.objects.filter(due_date=date_obj)
        except (IndexError, ValueError):
            pass

        return queryset, use_distinct


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_id', 'date_start', 'date_end')
    search_fields = ('name', 'user_id__username')
    list_filter = ('date_start', 'date_end')
    date_hierarchy = 'date_start'
    ordering = ('id',)


admin.site.register(TodoTask, TodoTaskAdmin)
admin.site.register(TodoItem, TodoItemAdmin)
admin.site.register(Project, ProjectAdmin)
