from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.post_create, name='post-create'),
    path('edit/<pk>', views.post_edit, name='post-edit'),
    path('post/<pk>', views.PostDetailView.as_view(), name='post-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
