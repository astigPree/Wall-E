from django.db import models
from django.utils import timezone


# Create your models here.

class Nurse(models.Model):
    name = models.CharField(max_length=100 , default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    face = models.ImageField(upload_to='nurse_faces', blank=True, null=True, default=None) 
    
    def __str__(self):
        return f"{self.name} -> {self.date_added}"
    
    
class Patient(models.Model):
    name = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    middle_name = models.CharField(max_length=100, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    face = models.ImageField(upload_to='patient_faces', blank=True, null=True, default=None)
    
    def __str__(self):
        return f"{self.name} -> {self.date_added}"
    
    
class Schedule(models.Model):
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
    
    