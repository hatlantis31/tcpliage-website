# metal_api/urls.py (App-level URLs)
from django.urls import path
from . import views

app_name = 'metal_api'

urlpatterns = [
    # Shape endpoints
    path('shapes/', 
         views.get_shapes, 
         name='shapes-list'),
    
    path('shapes/<str:shape_id>/config/', 
         views.get_shape_config, 
         name='shape-config'),
    
    # Design endpoints
    path('designs/', 
         views.save_design, 
         name='save-design'),
    
    path('designs/<int:design_id>/', 
         views.get_design, 
         name='get-design'),
    
    path('validate-design/', 
         views.validate_design, 
         name='validate-design'),
]
