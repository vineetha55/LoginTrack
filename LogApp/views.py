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
    total_emp=tbl_Employees.objects.all().count()
    total_atte= 0 if tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today()).first()==None else tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today()).first().count()
    return render(request,"Admin_Dashboard.html",{"total_emp":total_emp,"total_atte":total_atte})


def profile(request):
    d=tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request,"profile.html",{"d":d})

def sign_out(request):
    del request.session['admin_id']
    return redirect("/")
def add_employees(request):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request,"add_employees.html",{"d":d})
def save_employee(request):
    if request.method=="POST":
        obj=tbl_Employees()
        obj.name=request.POST.get("name")
        obj.email=request.POST.get("email")
        obj.mobile=request.POST.get("mobile")
        obj.password=request.POST.get("password")
        obj.joining_date = request.POST.get("join_date")
        obj.save()
        return redirect("/view_employee/")

def view_employee(request):
    data=tbl_Employees.objects.all()
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request,"view_employee.html",{"data":data,"d":d})

def login_info(request):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    data=tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today())
    emp_list=tbl_Employees.objects.all()
    return render(request,"login_info.html",{"data":data,"d":d,"emp_list":emp_list})

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
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    r=tbl_member_arrival_and_left_time_details.objects.get(id=id)
    return render(request,"full_details.html",{"r":r,"d":d})


def edit_emp(request,id):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    d1=tbl_Employees.objects.get(id=id)
    return render(request,"edit_emp.html",{"d":d,"d1":d1})

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
    emp=tbl_Employees.objects.get(id=id)
    d=tbl_member_arrival_and_left_time_details.objects.filter(emp_id=id)
    return render(request,"login_info_emp.html",{"d":d,"emp":emp})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
  # Adjust to your actual model import




from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import tbl_Employees, IdleSession

@csrf_exempt
def idle_notification_api(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("username", False)
            password = request.POST.get("password", False)
            idle_start = request.POST.get('idle_start', False)
            idle_end = request.POST.get('idle_end', False)
            total_idle_minutes = request.POST.get('total_idle_time', False)

            # Log received data for debugging
            print(username, password, idle_start, idle_end, total_idle_minutes)

            # Retrieve user instance
            user = tbl_Employees.objects.get(name=username, password=password)

            # Convert received data to appropriate formats
            idle_start_time = datetime.fromisoformat(idle_start)
            idle_end_time = datetime.fromisoformat(idle_end)

            # Parse the idle time in minutes and convert to timedelta
            idle_minutes = int(total_idle_minutes.split()[0])  # Extract minutes as integer
            total_idle_time = timedelta(minutes=idle_minutes)

            # Save the idle session data
            IdleSession.objects.create(
                user=user,
                date=idle_start_time.date(),
                idle_start=idle_start_time,
                idle_end=idle_end_time,
                total_idle_time=total_idle_time
            )

            return JsonResponse({'message': 'Idle session recorded successfully.'}, status=200)

        except tbl_Employees.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except (ValueError, IndexError) as e:
            print("Error parsing data:", e)
            return JsonResponse({'error': 'Invalid date/time or idle time format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




def Month_filter_Employee(request):
    d=tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    month=request.POST.get("month")
    year,month=month.split("-")
    emp=request.POST.get("employee")
    emp_list = tbl_Employees.objects.all()
    data=tbl_member_arrival_and_left_time_details.objects.filter(dt__month=int(month),emp_id=emp,dt__year=int(year))
    return render(request,"login_info.html",{"d":d,"data":data,"emp_list":emp_list})


def yesterday_attendance(request):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    yesterday = timezone.now() - timedelta(days=1)
    # Format the date if needed
    yesterday_date = yesterday.date()
    emp_list = tbl_Employees.objects.all()
    data = tbl_member_arrival_and_left_time_details.objects.filter(dt=yesterday_date)
    return render(request, "login_info.html", {"d": d, "data": data, "emp_list": emp_list})


def date_filter(request):
    date=request.POST.get("date")
    data=tbl_member_arrival_and_left_time_details.objects.filter(dt=date)
    emp_list = tbl_Employees.objects.all()
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request, "login_info.html", {"d": d, "data": data, "emp_list": emp_list})

def month_filter(request):
    month=request.POST.get("month")
    year, month = month.split("-")
    data = tbl_member_arrival_and_left_time_details.objects.filter(dt__month=int(month),dt__year=int(year))
    emp_list = tbl_Employees.objects.all()
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request, "login_info.html", {"d": d, "data": data, "emp_list": emp_list})

def current_month(request):
    m=date.today()
    data=tbl_member_arrival_and_left_time_details.objects.filter(dt__month=m.month)
    emp_list = tbl_Employees.objects.all()
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request, "login_info.html", {"d": d, "data": data, "emp_list": emp_list})


def update_admin(request):
    g=tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    g.username=request.POST.get("username")
    g.password=request.POST.get("password")
    g.email=request.POST.get("email")
    g.mobile=request.POST.get("mobile")
    g.save()
    return redirect("/profile/")

def view_all_admins(request):
    data=tbl_Registration_Details.objects.all().exclude(id=request.session['admin_id'])
    d=tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request,"view_all_admins.html",{"data":data,"d":d})


def idle_time_view(request):
    data=IdleSession.objects.all()
    return render(request,"idle_time_view.html",{"data":data})