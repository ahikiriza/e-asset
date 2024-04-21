from django.contrib import admin
from .models import *

#register asset models 
@admin.register(Staff)
class DisplayStaff(admin.ModelAdmin):
    list_display =Staff.Display_Staff

@admin.register(Agency)
class DisplayAgency(admin.ModelAdmin):
    list_display = Agency.Display_Agency

@admin.register(Equipment)
class DisplayEquipment(admin.ModelAdmin):
    list_display =Equipment.Display_Equipment

@admin.register(MarketTransaction)
class DisplayMarketTransaction(admin.ModelAdmin):
    list_display = MarketTransaction.Display_MarketTransaction

@admin.register(Store)
class DisplayStore(admin.ModelAdmin):
    list_display =Store.Display_Store

@admin.register(DisposedComputer)
class DisplayDisposedComputers(admin.ModelAdmin):
    list_display =DisposedComputer.Display_DisposedComputer

@admin.register(Asset)
class DisplayAsset(admin.ModelAdmin):
    list_display =Asset.Display_Asset


# Register your models here.
# admin.site.register(Registration)
# admin.site.register(Login)
#Other model registrations
    
# @admin.register(Login)
# class LoginAdmin(admin.ModelAdmin):
#     list_display =Login.Display_Login_Fields

# @admin.register(Admin_Model)
# class Admin_ModelAdmin(admin.ModelAdmin):
#     list_display=Admin_Model.Display_Admins
    
# @admin.register(Role_Model)
# class Role_modelAdmin(admin.ModelAdmin):
#     list_display=Role_Model.Display_Roles
    
# @admin.register(Supportstaff)
# class SupportstaffAdmin(admin.ModelAdmin):
#     list_display=Supportstaff.Display_Supportstaff
    
# @admin.register(Student)
# class MyClass(admin.ModelAdmin):
#     list_display = Student.Display_Fields

# @admin.register(Subjects)
# class Displaysubject(admin.ModelAdmin):
#     list_display = Subjects.Display_Subjects

# @admin.register(Schoolclasses)
# class Displayclasses(admin.ModelAdmin):
#     list_display = Schoolclasses.Display_schoolclasses
    
# @admin.register(Teachers)
# class Displayteachers(admin.ModelAdmin):
#     list_display = Teachers.Display_Teachers
    
# @admin.register(Marks)
# class Displayprimaryonemarks(admin.ModelAdmin):
#     list_display = Marks.displaymarks
    

# @admin.register(Administrators)
# class Displayadministrators(admin.ModelAdmin):
#     list_display = Administrators.displayadministrators
    
    
    
    
    
    
    
    
    
    