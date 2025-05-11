from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Nurse)

admin.site.register(Patient)

admin.site.register(Schedule)

admin.site.register(Account)

admin.site.register(LockingLogs)