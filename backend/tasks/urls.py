#from django.urls import path, include
#from rest_framework.routers import DefaultRouter
#from . import views

#router = DefaultRouter()
#router.register(r'tasks', views.TaskViewSet, basename='task')

#urlpatterns = [
#    path('', include(router.urls)),
 #   path('tasks/analyze/', views.analyze_tasks, name='analyze-tasks'),
  #  path('tasks/suggest/', views.suggest_tasks, name='suggest-tasks'),
   # path('health/', views.health_check, name='health-check'),
   # path('strategies/', views.TaskAnalysisView.as_view(), name='strategies'),
#]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    # Custom endpoints BEFORE the router
    path('tasks/analyze/', views.analyze_tasks, name='analyze-tasks'),
    path('tasks/suggest/', views.suggest_tasks, name='suggest-tasks'),
    path('health/', views.health_check, name='health-check'),
    path('strategies/', views.TaskAnalysisView.as_view(), name='strategies'),
    
    # Router patterns AFTER custom endpoints
    path('', include(router.urls)),
]