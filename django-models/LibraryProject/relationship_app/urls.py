from django.urls import path
from .views import list_books, LibraryDetailView, path
from .views import login_view, logout_view, register_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
]

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),  # Your custom registration view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

]