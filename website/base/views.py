from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from .models import Account, Nurse, Patient, Schedule, LockingLogs
from datetime import datetime
import requests




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

def nurse_page(request, nurse_id : int):
    
    if not request.user.is_authenticated:
        return redirect('index')
    try:
        nurse = Nurse.objects.get(id=nurse_id)
        if nurse.account_id != request.user.id:
            logout(request)
            return redirect('index')
        nurse_data = nurse.get_nurse_data() 
        return render(request, 'nurse_page.html' , context={'nurse' : nurse_data})
    
    except Nurse.DoesNotExist:
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
            phonenumber = request.POST.get('phone_number')
            color = request.POST.get('color')
            
            if not first_name or not last_name or not middle_name or not face or not phonenumber and not color:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            # Create a new patient object
            patient = Patient.objects.create(
                name = f"{first_name} {middle_name[0].upper()}. {last_name}",
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                account_id=request.user.id,
                face=face,
                phone_number=phonenumber,
                color_location=color
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
            
            patient_id = request.POST.get('patient_id')
            medication_time = request.POST.get('medication_time')
            medication_type = request.POST.get('medication_type')
            
            if not medication_time or not medication_type or not patient_id:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            medication_time = datetime.strptime(medication_time, '%H:%M').time()
            
            # Create a new schedule object
            schedule = Schedule.objects.create(
                patient = patient_id,
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
            patient_id = request.POST.get('patient_id')
            
            if not medication_time or not medication_type or not medication_date or not patient_id:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            medication_date = datetime.strptime(medication_date, '%Y-%m-%d').date()
            medication_time = datetime.strptime(medication_time, '%H:%M').time()
            
            # Create a new schedule object
            schedule = Schedule.objects.create(
                patient = patient_id,
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
            
            schedules = Schedule.objects.filter(patient=patient_id)
            for schedule in schedules:
                schedule.delete()
            
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


def get_patient_medications(request, patient_id ):
    try:
        if request.method == "GET" and request.user.is_authenticated:
            patient = Patient.objects.filter(id=patient_id).first()

            if not patient:
                return JsonResponse({'error': 'Patient not found'}, status=404)

            if patient.account_id != request.user.id:
                return JsonResponse({'error': 'Patient not found'}, status=404)
            
            schedules = Schedule.objects.filter(patient=patient_id).order_by('-created_at')
            medications = [
                schedule.get_schedule_data() for schedule in schedules
            ]
            
            return JsonResponse({
                'medications': medications
            }, status=200)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def delete_schedule(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            schedule_id = request.POST.get('schedule_id')
            schedule = Schedule.objects.filter(id=schedule_id).first()

            if not schedule:
                return JsonResponse({'error': 'Schedule not found'}, status=404)

            if schedule.account_id != request.user.id:
                return JsonResponse({'error': 'Schedule not found'}, status=404)

            schedule.delete()

            return JsonResponse({'message': 'Schedule deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)   


def nurse_locking_data(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            nurse_id = request.POST.get('nurse_id')
            nurse = Nurse.objects.filter(id=int(nurse_id)).first()
            date = request.POST.get('date', None)
            if not nurse or not date:
                return JsonResponse({'error': 'Nurse not found'}, status=404)
            
            converted_date = datetime.strptime(date, '%Y-%m-%d').date()
            print("Converted Date:", converted_date)

            log_objs = LockingLogs.objects.filter(nurse_id=nurse_id , created_at__date=converted_date)
            logs = [log.get_locking_logs_data() for log in log_objs] 
            
            return JsonResponse({'message': 'Nurse locked successfully' , 'logs' : logs}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# ======================= CONTROLLERS ========================

@csrf_exempt
def controller_get_data(request):
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            patients = Patient.objects.filter(account_id=user.user_id)
            nurses = Nurse.objects.filter(account_id=user.user_id)
            schedules = Schedule.objects.filter(account_id=user.user_id)
            
            patients_data = {
                patient.pk : patient.get_patient_data() for patient in patients
            }
            nurses_data = {
                nurse.pk : nurse.get_nurse_data() for nurse in nurses
            }
            schedules_data = {
                schedule.pk : schedule.get_schedule_data() for schedule in schedules
            }
            
            return JsonResponse({
                'patients': patients_data,
                'nurses': nurses_data,
                'schedules': schedules_data
            }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
    

@csrf_exempt
def controller_delete_schedule(request):
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            schedule_id = request.POST.get('schedule_id' , None)
            if not schedule_id:
                return JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched = Schedule.objects.filter(account_id = user.user_id , id=schedule_id).first()
            if not sched:
                raise JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched.delete()
            
            return JsonResponse({
                'success': 'Schedule deleted'
            }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def controller_taken_medicine_schedule(request):
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            schedule_id = request.POST.get('schedule_id' , None)
            if not schedule_id:
                return JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched = Schedule.objects.filter(account_id = user.user_id , id=schedule_id).first()
            if not sched:
                raise JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched.is_medication_taken = True
            sched.save()
            
            return JsonResponse({
                'success': 'Schedule Medication taken successfully'
            }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def controller_reset_taken_medicine(request):
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            schedule_id = request.POST.get('schedule_id' , None)
            if not schedule_id:
                return JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched = Schedule.objects.filter(account_id = user.user_id , id=schedule_id).first()
            if not sched:
                raise JsonResponse({'error': 'Schedule not found'}, status=404)
            
            sched.is_medication_taken = False
            sched.save()
            
            return JsonResponse({
                'success': 'Schedule Medication taken successfully'
            }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)






@csrf_exempt
def notify_medication(request):
    
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            patient_id = request.POST.get('patient_id' , None)
            if not patient_id:
                return JsonResponse({'error': 'Patient not found'}, status=404)
            
            patient = Patient.objects.filter(id=patient_id, account_id=user.user_id).first()
            if not patient:
                return JsonResponse({'error': 'Patient not found'}, status=404)
            
            # TODO: Message the emergency number
            url = ""
            params = {
                "api_token": "",
                "message": "",
                "phone_number": "",
            }
            
            response = requests.post(url, data=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to send notification: {response.text}")
            
            response_json = response.json()
            if response_json.get("status", None) != 200:
                raise Exception(f"Failed to send notification: {response_json.get('message', None)}")
            
            return JsonResponse({
                'success': 'Currently Messaging the Patient Emergency Number'
            }, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def controller_nurse_locking_log(request):
    try:
        
        if request.method == "POST":
            controller_token = request.POST.get('controller_token')
            
            user = Account.objects.filter(user_token=controller_token).first()
            print("controller ; ", controller_token)
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            nurse_id = request.POST.get('nurse_id' , None)
            if not nurse_id:
                return JsonResponse({'error': 'Nurse not found'}, status=404)
            
            nurse = Nurse.objects.filter(id=int(nurse_id)).first()
            if not nurse:
                return JsonResponse({'error': 'Nurse not found'}, status=404)
            
            is_for_lock = request.POST.get('is_for_lock', None)
            if not isinstance(is_for_lock, bool):
                return JsonResponse({'error': 'is_for_lock not found'}, status=404)
            
            LockingLogs.objects.create(
                nurse_id=nurse_id,
                is_for_lock=is_for_lock,
                logs = "Nurse locked the machine" if is_for_lock else "Nurse unlocked the machine",
            )
            
            return JsonResponse({
                'success': 'Created Nurse Locking Log successfully'
            }, status=200)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)