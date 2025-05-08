from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
]

# Aici adaugă ruta pentru static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
