from django.contrib import admin
from .models import Recipe, Rating, Comment

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "created_at")
	search_fields = ("title", "description", "ingredients")
	list_filter = ("created_at", "author")

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ("user", "recipe", "value")
	list_filter = ("value", "recipe")
	search_fields = ("user__username", "recipe__title")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("user", "recipe", "created_at")
	search_fields = ("user__username", "recipe__title", "text")
	list_filter = ("created_at", "recipe")
