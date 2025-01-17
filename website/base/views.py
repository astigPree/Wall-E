from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'homepage.html')

def login_user(request):
    return JsonResponse({'error': 'You must be authenticated to view this page.'})

def datamanager_page(request):
    return render(request, 'datamanager_page.html')

def patient_page(request):
    return render(request, 'patient_page.html')