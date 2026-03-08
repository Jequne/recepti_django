from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:pk>/rate/', views.ajax_rate_recipe, name='ajax_rate_recipe'),
    path('recipe/<int:pk>/comment/', views.ajax_add_comment, name='ajax_add_comment'),
]
