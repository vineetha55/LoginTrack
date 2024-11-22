import json
from datetime import date, time

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
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
    total_atte= 0 if tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today()).first()==None else tbl_member_arrival_and_left_time_details.objects.filter(dt=date.today()).count()
    return render(request,"Admin_Dashboard.html",{"total_emp":total_emp,"total_atte":total_atte,'current_date': datetime.now().strftime('%Y-%m-%d')})


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
        obj.start_time = request.POST.get("start_time")
        obj.end_time = request.POST.get("end_time")
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
                current_hour = now.hour  # Extract hour to determine morning or noon login

                morning_start_time = data_login.start_time
                temp_datetime = datetime.combine(datetime.today(), morning_start_time)
                new_datetime = temp_datetime + timedelta(minutes=1)
                morning_start_time = new_datetime.time()
                noon_start_time = time(13, 46)
                arrival_time = timezone.now().time()


                if current_hour < 13:
                    session_start_time = morning_start_time
                elif 13 < current_hour < 18:
                    session_start_time = noon_start_time
                else:
                    session_start_time="None"


                # Check if arrival time is before or equal to the session start time
                if session_start_time == "None":
                    arrival_status="Not Updated"
                elif arrival_time <= session_start_time:
                    arrival_status = "On Time"
                else:
                    arrival_status = "Late"

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
                    arrival_status=arrival_status

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
        current_time = timezone.now().time()

        noon_end_time = time(13, 9)
        evening_end_time = emp_record.end_time
        temp_datetime = datetime.combine(datetime.today(), evening_end_time)
        new_datetime = temp_datetime - timedelta(minutes=1)
        evening_end_time=new_datetime.time()
        now=datetime.now()
        current_hour = now.hour
        if 13< current_hour <18:
            session_start_time="None"
        elif current_time <= noon_end_time:
            session_start_time = noon_end_time
        else:
            session_start_time = evening_end_time

        # Check if arrival time is before or equal to the session start time
        if session_start_time=="None":
            left_status="Not Updated"
        elif current_time <= session_start_time:
            left_status = "Before time"
        else:
            left_status = "On Time"
        if latest_entry:
            latest_entry.left_time = timezone.now().time()
            latest_entry.login_status = "Logged Out"
            latest_entry.left_status=left_status
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
    obj.joining_date = request.POST.get("join_date")
    obj.start_time = request.POST.get("start_time")
    obj.end_time = request.POST.get("end_time")
    obj.save()
    return redirect("/view_employee/")

def delete_emp(request,id):
    obj=tbl_Employees.objects.get(id=id)
    obj.delete()
    return redirect("/view_employee/")
def delete_idle(request,id):
    obj=IdleSession.objects.get(id=id)
    obj.delete()
    return redirect("/idle_time_view/")
def edit_login(request,id):
    obj=tbl_member_arrival_and_left_time_details.objects.get(id=id)
    return render(request,"edit_login.html",{"obj":obj})
def delete_login(request,id):
    obj=tbl_member_arrival_and_left_time_details.objects.get(id=id)
    obj.delete()
    return redirect("/login_info/")


def update_login(request,id):
    obj=tbl_member_arrival_and_left_time_details.objects.get(id=id)
    if request.POST.get("arrival_time") == '':
        obj.arrival_time = None
    else:
        obj.arrival_time = request.POST.get("arrival_time")
    if request.POST.get("left_time") == '':
        obj.left_time=None
    else:
        obj.left_time = request.POST.get("left_time")
    obj.login_status=request.POST.get("login_status")
    obj.arrival_status=request.POST.get("arrival_status")
    obj.left_status=request.POST.get("left_status")
    obj.save()
    return redirect("/login_info/")
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
from .utils import send_sms
@csrf_exempt
def idle_notification_api(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("username", False)
            password = request.POST.get("password", False)
            idle_start = request.POST.get('idle_start', False)
            idle_end = request.POST.get('idle_end', False)
            total_idle_minutes = request.POST.get('total_idle_time', False)
            print("hello")

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
            message = (
                f"Idle Time Alert:\n"
                f"User: {user.name}\n"
                f"Date: {idle_start_time.date()}\n"
                f"Idle Start: {idle_start_time}\n"
                f"Idle End: {idle_end_time}\n"
                f"Total Idle Time: {total_idle_time}"
            )

            # Send SMS to admin
            send_sms(settings.ADMIN_PHONE_NUMBER, message)
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
    data=IdleSession.objects.all().order_by('-id')
    emp_list=tbl_Employees.objects.all()
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    return render(request,"idle_time_view.html",{"data":data,"d":d,"emp_list":emp_list})

def idle_filter_emp(request):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    month = request.POST.get("month")
    year, month = month.split("-")
    emp = request.POST.get("employee")
    emp_list = tbl_Employees.objects.all()
    data = IdleSession.objects.filter(date__month=int(month), user=emp, date__year=int(year))
    return render(request, "idle_time_view.html", {"d": d, "data": data, "emp_list": emp_list})



def save_reason(request):
    if request.method == "POST":
        data = json.loads(request.body)
        row_id = data.get("row_id")
        reason = data.get("reason")

        try:
            row = IdleSession.objects.get(id=row_id)
            row.reason = reason  # Update the reason field
            row.save()
            return JsonResponse({"success": True})
        except IdleSession.DoesNotExist:
            return JsonResponse({"success": False, "error": "Row not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


def monthly_log_status(request):
    d=tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    emp_list=tbl_Employees.objects.all()
    return render(request,"monthly_log_status.html",{"d":d,"emp_list":emp_list})


def monthly_log_status1(request):
    d = tbl_Registration_Details.objects.get(id=request.session['admin_id'])
    month = request.POST.get("month")
    print(month,"jj")

    emp = request.POST.get("employee")
    if emp =="Select any Employee":
        messages.error(request,"Please select an Employee")
        return redirect("/monthly_log_status/")
    if not month :
        messages.error(request,"Please select a Month")
        return redirect("/monthly_log_status/")
    year, month = month.split("-")
    emp_list = tbl_Employees.objects.all()
    data = tbl_member_arrival_and_left_time_details.objects.filter(dt__month=int(month), emp_id=emp, dt__year=int(year))
    total_late = data.filter(arrival_status="Late").count()
    total_early = data.filter(left_status="Before time").count()
    return render(request,"monthly_log_status.html",{"d":d,"emp_list":emp_list,"data":data,
                                                     "total_late":total_late,"total_early":total_early})
import csv

def download_csv(request):
    # Create the HttpResponse object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="table_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Employee name', 'Arrival Time', 'Left time','Date','Arrival status','Left Status'])  # Replace with your actual column names

    # Write data rows
    for obj in tbl_member_arrival_and_left_time_details.objects.all():
        print(obj.arrival_time)
        writer.writerow([obj.emp_id.name, obj.arrival_time, obj.left_time,obj.dt,obj.arrival_status,obj.left_status])  # Replace field names with your model's fields

    return response
