from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('edit/<pk>', views.PostEditView.as_view(), name='post-edit'),
    path('delete/<pk>', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<pk>', views.PostDetailView.as_view(), name='post-detail'),

    path('login/', views.LoginFormView.as_view(), name='login'),
    path('reg/', views.RegisterFormView.as_view(), name='registration'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
