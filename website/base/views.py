from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Account, Nurse, Patient, Schedule

def index(request):
    return render(request, 'homepage.html') 


def login_user(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login the user
                login(request, user)
                # Redirect to a success page
                return JsonResponse({'url' : '/datamanager'}, status=200)
            else:
                # Invalid login 
                return JsonResponse({'error' : 'Invalid username or password'}, status=400)

        # If GET request, render login page
        return render(request, 'login.html')
    
    except Exception as e:
        return redirect('index')

    

def datamanager_page(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('index')
    
    print(request.user.id)
    # Render the data manager page if authenticated
    
    return render(request, 'datamanager_page.html')

def patient_page(request):
    return render(request, 'patient_page.html')


def fetch_patients_data(request):
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                # Fetch patient data from the database
                patients = Patient.objects.filter(account_id=request.user.id).order_by('-date_added')
                patients_data = [
                    patient.get_patient_data() for patient in patients
                ]
                
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def fetch_nurses_data(request):
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                # Fetch nurse data from the database
                nurses = Nurse.objects.filter(account_id=request.user.id).order_by('-date_added')
                nurses_data = [
                    nurse.get_nurse_data() for nurse in nurses
                ]
                
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


