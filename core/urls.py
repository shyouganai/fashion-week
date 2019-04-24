from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('create/', views.post_create, name='post-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
