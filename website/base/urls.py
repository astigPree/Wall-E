

from django.urls import path

from. import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('datamanager', views.datamanager_page, name='datamanager_page'),
    path('patient', views.patient_page, name='patient_page'),
    
    
    
    path('fetch/patients', views.fetch_patients_data, name='fetch_patients'),
    path('fetch/nurses', views.fetch_nurses_data, name='fetch_nurses'),
    
    path('create/patient', views.add_patient, name='create_patient'),
    path('create/nurse', views.add_nurse, name='create_nurse'),
    
]