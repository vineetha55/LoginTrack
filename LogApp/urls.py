from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("save_admin/",views.save_admin,name="save_admin"),
    path("check_login/",views.check_login,name="check_login"),
    path("Admin_Dashboard/",views.Admin_Dashboard,name="Admin_Dashboard"),
    path("add_employees/",views.add_employees,name="add_employees"),
    path("save_employee/",views.save_employee,name="save_employee"),
    path("view_employee/",views.view_employee,name="view_employee"),
    path("login_info/",views.login_info,name="login_info"),
    path("desktop_app_login_api/",views.desktop_app_login_api,name="desktop_app_login_api"),
    path("desktop_app_logout_api/",views.desktop_app_logout_api,name="desktop_app_logout_api"),
    path("full_details/<id>",views.full_details,name="full_details"),
    path("edit_emp/<id>",views.edit_emp,name="edit_emp"),
    path("update_employee/<id>",views.update_employee,name="update_employee"),
    path("delete_emp/<id>",views.delete_emp,name="delete_emp"),
    path("login_info_emp/<id>",views.login_info_emp,name="login_info_emp"),
    path('idle_notification_api/', views.idle_notification_api, name='idle_notification_api'),
    path("profile/",views.profile,name="profile"),
    path("sign_out/",views.sign_out,name="sign_out"),
    path("Month-filter-Employee/",views.Month_filter_Employee,name="Month-filter-Employee"),
    path("yesterday_attendance/",views.yesterday_attendance,name="yesterday_attendance"),
    path("date_filter/",views.date_filter,name="date_filter"),
    path("month_filter/",views.month_filter,name="month_filter"),
    path("current_month/",views.current_month,name="current_month"),
    path("update_admin/",views.update_admin,name="update_admin"),
    path("view_all_admins/",views.view_all_admins,name="view_all_admins")
]