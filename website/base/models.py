from django.db import models
from django.utils import timezone 

# Create your models here.
def local_timezone():
    return timezone.localtime(timezone.now())

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    user_id = models.BigIntegerField(null=True, default=None, unique=True)
    user_token = models.CharField(max_length=100, null=True, default=None)
    
    def __str__(self):
        return self.username

class Nurse(models.Model):
    account_id = models.BigIntegerField(null=True, default=None)
    name = models.CharField(max_length=100 , default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    date_added = models.DateTimeField( default=local_timezone)
    face = models.ImageField(upload_to='nurse_faces', blank=True, null=True, default=None) 
    
    def __str__(self):
        return f"{self.pk} : {self.name} -> {self.date_added}"
    
    def get_nurse_data(self):
        data =  {
            'id': self.pk,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name, 
            'face': self.face.url if self.face else None
        }
        
        local_created_at = timezone.localtime(self.date_added)
        #data['created_at'] = local_created_at.strftime('%Y-%m-%d %H:%M:%S %p')
        data['date_added'] = local_created_at.strftime('%Y-%m-%d %I:%M:%S %p')
        return data
    
    
class Patient(models.Model):
    account_id = models.BigIntegerField(null=True, default=None)
    name = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    date_added = models.DateTimeField( default=local_timezone)
    face = models.ImageField(upload_to='patient_faces', blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=100, null=True, default=None)
    color_location = models.CharField(max_length=50, default=None, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk} : {self.name} -> {self.date_added}"
    
    def get_patient_data(self):
        data = {
            'id': self.pk,
            'name': self.name,
            'color': self.color_location,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name, 
            'face': self.face.url if self.face else None,
            'phone_number': self.phone_number
        }
                
        local_created_at = timezone.localtime(self.date_added)
        #data['created_at'] = local_created_at.strftime('%Y-%m-%d %H:%M:%S %p')
        data['date_added'] = local_created_at.strftime('%Y-%m-%d %I:%M:%S %p')
        return data
    
    
class Schedule(models.Model):
    account_id = models.BigIntegerField(null=True, default=None)
    nurse = models.BigIntegerField( blank=True, null=True, default=None)
    patient = models.BigIntegerField( blank=True, null=True, default=None)
    created_at = models.DateField(auto_now_add=True )
    pill = models.CharField(max_length=20 , blank=True, null=True, default=None) 
    is_daily = models.BooleanField(default=False)
    is_medication_taken = models.BooleanField(default=False)
    set_date = models.DateField(blank=True, null=True, default=None)
    set_time = models.TimeField(blank=True, null=True, default=None)
    
    
    def __str__(self):
        return f"{self.nurse} -> {self.patient} -> {self.created_at} -> {self.pill} -> { 'daily' if self.is_daily else 'once' }"
    
    
    def get_schedule_data(self):
        return {
            'id': self.pk,
            'nurse': self.nurse,
            'patient': self.patient,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'pill': self.pill,
            'is_daily': self.is_daily,
            'is_medication_taken': self.is_medication_taken,
            'set_date': self.set_date.strftime("%Y-%m-%d") if self.set_date else None,
            'set_time': self.set_time.strftime("%H:%M") if self.set_time else None
        }
        
        
class LockingLogs(models.Model):
    nurse_id = models.BigIntegerField(null=True, default=None)
    created_at = models.DateTimeField( default=local_timezone)
    logs = models.CharField(max_length=200 , blank=True, null=True, default=None)
    is_for_locking = models.BooleanField(default=True) # True for locking, False for unlocking
    
    def __str__(self):
        return f"{self.nurse_id} -> {self.created_at} -> {self.logs}"
    
    def get_locking_logs_data(self):
        data = {
            'id': self.pk,
            'nurse_id': self.nurse_id, 
            'logs': self.logs,
            'is_for_locking': self.is_for_locking
        }
        local_created_at = timezone.localtime(self.created_at)
        #data['created_at'] = local_created_at.strftime('%Y-%m-%d %H:%M:%S %p')
        data['created_at'] = local_created_at.strftime('%Y-%m-%d %I:%M:%S %p')
        return data

