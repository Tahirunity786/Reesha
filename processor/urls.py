
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from processor.views import main
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name="HOME"), 
    path('core/', include('core.urls'))
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
