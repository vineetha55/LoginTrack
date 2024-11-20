from datetime import datetime

from django.db import models

# Create your models here.
class tbl_Registration_Details(models.Model):
    username=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    mobile=models.IntegerField(null=True)
    password=models.CharField(max_length=100,null=True)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

class tbl_Employees(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    mobile = models.IntegerField(null=True)
    password = models.CharField(max_length=100, null=True)
    joining_date=models.DateField(null=True)
    start_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)


class tbl_member_arrival_and_left_time_details(models.Model):
    emp_id = models.ForeignKey(tbl_Employees,on_delete=models.CASCADE,related_name="member_arrival_and_left_time_details_member_id", null=True)
    arrival_time = models.TimeField(null=True,blank=True)
    left_time = models.TimeField(null=True,blank=True)
    arrival_status=models.CharField(max_length=255, null=True)
    left_status=models.CharField(max_length=255, null=True)
    public_ip = models.CharField(max_length=255, null=True)
    private_ip = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255, null=True)
    country_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    postal = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    ip_type = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    current_machine_id = models.TextField(null=True)
    login_status = models.CharField(max_length=255,null=True)
    login_system_ip_address = models.CharField(max_length=255,null=True)
    login_system_name= models.CharField(max_length=255,null=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True)

class IdleSession(models.Model):
    user = models.ForeignKey(tbl_Employees, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    idle_start = models.DateTimeField()
    idle_end = models.DateTimeField()
    total_idle_time = models.DurationField()
    reason=models.TextField(null=True)