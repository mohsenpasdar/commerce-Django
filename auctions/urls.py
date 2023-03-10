from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listings/<int:listing_id>/', views.listing, name='listing'),
    path('listing/<int:listing_id>/close_bid/', views.close_bid, name='close_bid'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<str:category_name>/', views.category, name='category'),
    
]

