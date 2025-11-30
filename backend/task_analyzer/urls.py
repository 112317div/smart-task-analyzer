#"""
#URL configuration for task_analyzer project.
#"""
#from django.contrib import admin
#from django.urls import path, include

#urlpatterns = [
 #   path('admin/', admin.site.urls),
  #  path('api/', include('tasks.urls')),
#]




from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
]

# Serve frontend in development
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        path('', lambda request: serve(request, 'index.html', 
             document_root=os.path.join(settings.BASE_DIR.parent, 'frontend'))),
    ]
