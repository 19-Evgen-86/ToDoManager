from django.contrib import admin

from goals.models import GoalsCategory, Goal, GoalComment


@admin.register(GoalsCategory)
class GoalsCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "create", "update"]
    search_fields = ["title", "user"]


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created", "updated", "category"]
    search_fields = ["title", "user", "category"]


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ["text",]
    search_fields = ["text"]
