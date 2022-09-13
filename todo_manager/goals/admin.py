from django.contrib import admin

from goals.models import GoalsCategory


class GoalsCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "create", "update"]
    search_fields = ["title", "user"]


admin.site.register(GoalsCategory, GoalsCategoryAdmin)
