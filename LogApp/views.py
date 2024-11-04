from datetime import date

from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import *
# Create your views here.
def index(request):
    return render(request,"index.html")

def signup(request):
    return render(request,"signup.html")
def signin(request):
    return render(request,"signin.html")

def save_admin(request):
    if request.method=="POST":
        obj=tbl_Registration_Details()
        obj.username=request.POST.get("username")
        obj.email=request.POST.get("email")
        obj.mobile=request.POST.get("mobile")
        obj.password=request.POST.get("password")
        obj.save()
        return redirect("/signin/")

def check_login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if tbl_Registration_Details.objects.filter(email=email,password=password).exists():
            v=tbl_Registration_Details.objects.get(email=email, password=password)
            request.session['admin_id']=v.id
            return redirect("/Admin_Dashboard/")
        else:
            return redirect("/signin/")

def Admin_Dashboard(request):
    return render(request,"Admin_Dashboard.html")

def add_employees(request):
    return render(request,"add_employees.html")
def save_employee(request):
    if request.method=="POST":
        obj=tbl_Employees()
        obj.name=request.POST.get("name")
        obj.email=request.POST.get("email")
        obj.mobile=request.POST.get("mobile")
        obj.password=request.POST.get("password")
        obj.save()
        return redirect("/view_employee/")

def view_employee(request):
    data=tbl_Employees.objects.all()
    return render(request,"view_employee.html",{"data":data})

def login_info(request):
    data=tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today())
    return render(request,"login_info.html",{"data":data})

@csrf_exempt
def desktop_app_login_api(request):
        if request.method == "POST":

            username = request.POST.get("username", False)
            password = request.POST.get("password", False)
            current_machine_id = request.POST.get("current_machine_id", False)
            hostname = request.POST.get("hostname", False)
            IPAddr = request.POST.get("IPAddr", False)
            public_ip = request.POST.get("public_ip", False)
            print("public_ip:::::::::::::", str(public_ip))

            response = requests.get("https://geolocation-db.com/json/" + str(public_ip) + "&position=true").json()

            country_code = response['country_code']
            country_name = response['country_name']
            city = response['city']
            postal = response['postal']
            latitude = response['latitude']
            longitude = response['longitude']

            ip_type = ""
            public_ip_addrees = ""
            try:
                public_ip_addrees = response['IPv4']
                ip_type = "IPv4"
            except:
                public_ip_addrees = response['IPv6']
                ip_type = "IPv6"

            state = response['state']

            print("country_code:::::::", str(country_code))
            print("country_name:::::", str(country_name))
            print("city:::::", str(city))
            print("postal::::", str(postal))
            print("latitude::::", str(latitude))
            print("longitude:::", str(longitude))
            print("iptype:::::", str(ip_type))
            print("public_ip_address:::", str(public_ip_addrees))

            print("username:::::::", str(username))
            print("password:::::", str(password))
            print("current_machine_id:::::::::::::", str(current_machine_id))
            data = {}

            try:
                data_login = tbl_Employees.objects.get(name=username, password=password)

                user_login_id = data_login.id
                # token_id = data_login.token


                from datetime import date

                today = date.today()

                from datetime import datetime

                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")

                member_login_log_save = tbl_member_arrival_and_left_time_details(
                    emp_id_id=user_login_id,
                    public_ip=public_ip_addrees,
                    private_ip=IPAddr,
                    country_code=country_code,
                    country_name=country_name,
                    city=city,
                    postal=postal,
                    latitude=latitude,
                    longitude=longitude,
                    ip_type=ip_type,
                    state=state,
                    status="True",
                    current_machine_id=current_machine_id,
                    login_status="login",
                    login_system_ip_address=IPAddr,
                    login_system_name=hostname,
                    arrival_time=timezone.now().time(),

                )
                member_login_log_save.save()



                print("user_login_id:::::::::", str(user_login_id))
                data['message'] = "success"
                data['token']=user_login_id

                return JsonResponse(data, safe=False)

            except:
                print("login error")
                data['message'] = "error"
                data['token'] = user_login_id
                return JsonResponse(data, safe=False)


OFFICE_LOCATION = (10.014554, 76.353587)  # Replace with your office's lat/lng
from geopy.distance import geodesic

def desktop_app_login_api1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Check if user is within 2 km of the office
        user_location = (latitude, longitude)
        print(user_location)
        distance_to_office = geodesic(user_location, OFFICE_LOCATION).km

        if distance_to_office > 2:
            return JsonResponse({"message": "Login not allowed outside 2 km radius of office."})

        # Continue with authentication and token handling
        # Perform username/password validation and return response
        # Generate a token function here
        return JsonResponse({"message": "success"})


    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def desktop_app_logout_api(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')

        emp_record = tbl_Employees.objects.get(name=username)

        # Get the most recent "Logged In" session without a logout time (left_time)
        latest_entry = tbl_member_arrival_and_left_time_details.objects.filter(
            emp_id=emp_record, login_status="login", left_time__isnull=True
        ).last()

        if latest_entry:
            latest_entry.left_time = timezone.now().time()
            latest_entry.login_status = "Logged Out"
            latest_entry.save()
            return JsonResponse({'message': 'Logout time recorded successfully.'})

        return JsonResponse({'message': 'No active session found.'}, status=400)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def full_details(request,id):
    r=tbl_member_arrival_and_left_time_details.objects.get(id=id)
    return render(request,"full_details.html",{"r":r})


def edit_emp(request,id):
    d=tbl_Employees.objects.get(id=id)
    return render(request,"edit_emp.html",{"d":d})

def update_employee(request,id):
    obj = tbl_Employees.objects.get(id=id)
    obj.name = request.POST.get("name")
    obj.email = request.POST.get("email")
    obj.mobile = request.POST.get("mobile")
    obj.password = request.POST.get("password")
    obj.save()
    return redirect("/view_employee/")

def delete_emp(request,id):
    obj=tbl_Employees.objects.get(id=id)
    obj.delete()
    return redirect("/view_employee/")

def login_info_emp(request,id):
    d=tbl_member_arrival_and_left_time_details.objects.filter(emp_id=id)
    return render(request,"login_info_emp.html",{"d":d})