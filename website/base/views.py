from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Account, Nurse, Patient, Schedule
from datetime import datetime

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
     
    # Render the data manager page if authenticated
    
    return render(request, 'datamanager_page.html')

def patient_page(request, patient_id : int):
    
    if not request.user.is_authenticated:
        return redirect('index')
    try:
        patient = Patient.objects.get(id=patient_id)
        if patient.account_id != request.user.id:
            logout(request)
            return redirect('index')
        patient_data = patient.get_patient_data() 
        return render(request, 'patient_page.html' , context={'patient' : patient_data})
    
    except Patient.DoesNotExist:
            logout(request)
            return redirect('index')


def fetch_patients_data(request):
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                # Fetch patient data from the database
                patients = Patient.objects.filter(account_id=request.user.id).order_by('-date_added')
                patients_data = [
                    patient.get_patient_data() for patient in patients
                ]
                
                return JsonResponse({
                    'patients': patients_data
                }, status=200)
                
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
                
                return JsonResponse({
                    'nurses': nurses_data
                }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_patient(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            face = request.FILES.get('face')
            
            if not first_name or not last_name or not middle_name or not face:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            # Create a new patient object
            patient = Patient.objects.create(
                name = f"{first_name} {middle_name[0].upper()}. {last_name}",
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                account_id=request.user.id,
                face=face
            )
            
            
            return JsonResponse({'message': 'Patient added successfully'}, status=200)
            
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_nurse(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            face = request.FILES.get('face')
            
            if not first_name or not last_name or not middle_name or not face:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            # Create a new nurse object
            nurse = Nurse.objects.create(
                name = f"{first_name} {middle_name[0].upper()}. {last_name}",
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                account_id=request.user.id,
                face=face
            )
            
            
            return JsonResponse({'message': 'Nurse added successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



def add_schedule_daily(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            
            medication_time = request.POST.get('medication_time')
            medication_type = request.POST.get('medication_type')
            
            if not medication_time or not medication_type:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            medication_time = datetime.strptime(medication_time, '%H:%M').time()
            
            # Create a new schedule object
            schedule = Schedule.objects.create(
                set_time=medication_time,
                pill=medication_type,
                account_id=request.user.id,
                is_daily = True,
            )
            
            return JsonResponse({'message': 'Schedule added successfully'}, status=200)
            
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
        
        
            

def add_schedule_once(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            
            medication_date = request.POST.get('medication_date')
            medication_time = request.POST.get('medication_time')
            medication_type = request.POST.get('medication_type')
            
            if not medication_time or not medication_type or not medication_date:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            medication_date = datetime.strptime(medication_date, '%Y-%m-%d').date()
            medication_time = datetime.strptime(medication_time, '%H:%M').time()
            
            # Create a new schedule object
            schedule = Schedule.objects.create(
                set_date = medication_date,
                set_time=medication_time,
                pill=medication_type,
                account_id=request.user.id, 
            )
            
            return JsonResponse({'message': 'Schedule added successfully'}, status=200)
            
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
        


def delete_patient(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            patient_id = request.POST.get('patient_id')
            patient =Patient.objects.filter(id=patient_id).first()
            
            if not patient:
                return JsonResponse({'error': 'Patient not found'}, status=404)
            
            if patient.account_id != request.user.id: 
                return JsonResponse({'error': 'Patient not found'}, status=404)
            
            patient.delete()
            
            return JsonResponse({'message': 'Patient deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



def delete_nurse(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            nurse_id = request.POST.get('nurse_id')
            nurse =Nurse.objects.filter(id=nurse_id).first()
            
            if not nurse:
                return JsonResponse({'error': 'Nurse not found'}, status=404)
            
            if nurse.account_id != request.user.id: 
                return JsonResponse({'error': 'Nurse not found'}, status=404)
            
            nurse.delete()
            
            return JsonResponse({'message': 'Nurse deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

