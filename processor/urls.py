
from django.contrib import admin
from django.urls import path, include
from processor.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="HOME"), 
    path('core/', include('core.urls'))
    
]
