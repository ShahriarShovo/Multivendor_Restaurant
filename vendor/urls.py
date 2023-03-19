from django.urls import path
from .import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendordashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menue_builder/', views.menue_builder, name='menue_builder'),
    path('menue_builder/cateroy/<int:pk>/',
          views.food_items_by_category, name='food_items_by_category'),

    #CRUD Category
    path('menue_builder/cateroy/add/', views.add_category, name='add_category'),
    path('menue_builder/cateroy/edit/<int:pk>/',
          views.edit_category, name='edit_category'),
    path('menue_builder/cateroy/delete/<int:pk>/',
          views.delete_category, name='delete_category'),




    #CRUD Food
    path('menue_builder/food/add/', views.add_food, name='add_food'),

    path('menue_builder/food/edit/<int:pk>/',
          views.edit_food, name='edit_food'),

    path('menue_builder/food/delete/<int:pk>/',
          views.delete_food, name='delete_food'),
]
