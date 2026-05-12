# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('result/', views.result, name='result'),
#     path('history/', views.history, name='history'),

#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
# path(
#     'admin-dashboard/update/<int:loan_id>/<str:decision>/',
#     views.update_loan_status,
#     name='update_loan_status'
# ),
# path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
# path('reject-loan/<int:loan_id>/', views.reject_loan, name='reject_loan'),
# # urls.py
# path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#  path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     path('admin-decision/<int:pk>/<str:decision>/', views.admin_decision, name='admin_decision'),
#     path('upload-model/', views.upload_model, name='upload_model'),
#     path('admin-history/', views.admin_history, name='admin_history'),
#     path(
#     'superuser-history/',
#     views.superuser_history,
#     name='superuser_history'
# ),
#  path('export/csv/', views.export_csv, name='export_csv'),
#     path('export/pdf/', views.export_pdf, name='export_pdf'),
#     path("superadmin/dashboard/", views.superadmin_dashboard, name="superadmin_dashboard"),
#     path(
#     'superadmin/history/',
#     views.system_history,
#     name='system_history'
# ),
# path('', views.index, name='home'),   # index.html as home
#     path('predict/', views.predict, name='predict'),
# ]


from django.urls import path
from . import views

urlpatterns = [

    # 🏠 LANDING PAGE
    path('', views.index, name='index'),

    # 🏠 ROLE BASED HOME (optional)
    path('home/', views.home, name='home'),

    # 📝 LOAN PREDICTION
    path('loan-form/', views.loan_form, name='loan_form'),

    path('result/', views.result, name='result'),
    path('history/', views.history, name='history'),

    # 🔐 AUTH
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 👨‍💼 ADMIN
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path(
        'admin-dashboard/update/<int:loan_id>/<str:decision>/',
        views.update_loan_status,
        name='update_loan_status'
    ),
    path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('reject-loan/<int:loan_id>/', views.reject_loan, name='reject_loan'),
    path('admin-decision/<int:pk>/<str:decision>/', views.admin_decision, name='admin_decision'),
    path('admin-history/', views.admin_history, name='admin_history'),

    # 👑 SUPER ADMIN
    path('upload-model/', views.upload_model, name='upload_model'),
    path('superuser-history/', views.superuser_history, name='superuser_history'),
    path('superadmin/dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/history/', views.system_history, name='system_history'),

    # 📤 EXPORTS
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path(
    'activate-model/<int:model_id>/',
    views.activate_model,
    name='activate_model'
),

path(
    'predict-loan/',
    views.predict_loan_api,
    name='predict_loan_api'
),

path(
    'loan-history/',
    views.loan_history_api,
    name='loan_history_api'
),
path('chatbot/', views.chatbot, name='chatbot'),
]
