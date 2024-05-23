from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.user_login, name="Admin Login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("register/", views.register, name="register"),
    path('dashboard/', views.home, name="Dashboard"),

    path('equipmentslist/', views.equipmentsList, name="EquipmentsList"),
    path('staffequipment/', views.staffEquipment, name="StaffEquipment"),
    path('allequipmentlist/', views.allEquipmentList, name="allEquipmentList"),
    path('addequipment/', views.equipmentsAdd, name="addEquipments"),
    path('addallequipment/', views.allEquipmentAdd, name="addallEquipment"),
    path('addequipment/submit/', views.equipmentReg, name="equipmentReg"),
    path('addallequipment/submit/', views.allEquipmentReg, name="allEquipmentReg"),
    path('addasset/', views.assetAdd, name="addAsset"),
    path('addasset/submit/', views.assetReg, name="assetReg"),
    path('assetlist/', views.assetList, name="AssetList"),

    # path('addteacher/', views.teacherAdd, name="Add Teacher"),
    path('marketequipment/', views.marketList, name="Market List"),

    path('retrieved-list/', views.retrievedList, name="RetrievedList"),
    path('disposed-equipment/', views.disposedEquipment, name="DisposedList"),
    path('agencyadd/', views.agencyAdd, name="AddAgency"),
    path('agencyadd/submit/', views.agencyReg, name="AgencyReg"),
    path('agency-list/', views.agencyList, name="ListAgency"),
    path('add-staff/', views.staffAdd, name="AddStaff"),
    path('add-staff/submit/', views.staffReg, name="StaffReg"),
    path('staff-list/', views.staffList, name="ListStaff"),


    # edit and delete  all equipment
    path('edit_equipment/', views.edit_equipment, name="edit_equipment"),
    path('delete_equipment/', views.delete_equipment, name="delete_equipment"),

    #edit and delete assets
    path('edit_asset/', views.edit_asset, name="edit_asset"),
    path('delete_asset/', views.delete_asset, name="delete_asset"),

    #edit and delete Staff
    path('edit_staff/', views.edit_staff, name="edit_staff"),
    path('delete_staff/', views.delete_staff, name="delete_staff"),

#     # settings urls
   path('edit_user_info/', views.edit_user_info, name='edit_user_info'),
#    path('create_user/', views.create_user, name='create_user'),
   path('settings/', views.create_user, name='create_user'),
   path('users/', views.display_users, name='display_users'),

    # imports
    path('export_equipment/', views.export_equipment_to_excel, name='export_equipment_to_excel'),
    path('import_equipment/', views.import_equipment, name='import_equipment'),

    #Events
    path('create_events/', views.create_Events, name='create_Events'),
    path('event_logs/', views.event_logs, name='event_logs'),


]















