from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('students/', views.student_list, name='student_list'),

    path('add/', views.add_student, name='add_student'),

    path('update/<int:id>/', views.update_student, name='update_student'),

    path('delete/<int:id>/', views.delete_student, name='delete_student'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('export-csv/', views.export_csv, name='export_csv'),

]