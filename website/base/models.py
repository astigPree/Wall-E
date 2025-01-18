from django.db import models
from django.utils import timezone


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
    date_added = models.DateTimeField(auto_now_add=True)
    face = models.ImageField(upload_to='nurse_faces', blank=True, null=True, default=None) 
    
    def __str__(self):
        return f"{self.name} -> {self.date_added}"
    
    def get_nurse_data(self):
        return {
            'id': self.pk,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'date_added': self.date_added.strftime("%Y-%m-%d %H:%M:%S"),
            'face': self.face.url if self.face else None
        }
    
    
class Patient(models.Model):
    account_id = models.BigIntegerField(null=True, default=None)
    name = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    face = models.ImageField(upload_to='patient_faces', blank=True, null=True, default=None)
    
    def __str__(self):
        return f"{self.name} -> {self.date_added}"
    
    def get_patient_data(self):
        return {
            'id': self.pk,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'date_added': self.date_added.strftime("%Y-%m-%d %H:%M:%S"),
            'face': self.face.url if self.face else None
        }
    
    
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