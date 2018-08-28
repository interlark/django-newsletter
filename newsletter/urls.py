from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('news.urls'), name='news'),
    # path('', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)