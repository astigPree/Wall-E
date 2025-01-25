

from django.urls import path

from. import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('datamanager', views.datamanager_page, name='datamanager_page'),
    path('patient/<int:patient_id>', views.patient_page, name='patient_page'),
    
    
    
    path('fetch/patients', views.fetch_patients_data, name='fetch_patients'),
    path('fetch/nurses', views.fetch_nurses_data, name='fetch_nurses'),
    
    path('create/patient', views.add_patient, name='create_patient'),
    path('create/nurse', views.add_nurse, name='create_nurse'),
    
    path('create/daily/medication', views.add_schedule_daily, name='add_schedule_daily'),
    path('create/once/medication', views.add_schedule_once, name='add_schedule_once'),
    
    path('delete/nurse' , views.delete_nurse, name='delete_nurse'),
    path('delete/patient' , views.delete_patient, name='delete_patient'),
    
    path('patient/medication/<int:patient_id>', views.get_patient_medications, name='patient_medications'),
    path('delete/medication', views.delete_schedule, name='delete_medications'),
    
    
    path("controller", views.controller_get_data, name='controller'),
    path("controller/delete", views.controller_get_data, name='controller_delete'),
    path("controller/taken", views.controller_get_data, name='controller_taken'),
    
]