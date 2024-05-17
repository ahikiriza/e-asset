from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib import messages
from .models import *
from django.db.models import Sum
from django.contrib.auth.models import User, Group
from .decorators import group_required
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, date
from django.utils.timezone import now
from django.db.models import Max
import openpyxl
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.db.models import Q  
import bcrypt
from django.core.exceptions import ValidationError
from django.utils import timezone

salt = bcrypt.gensalt()

def encryptpassword(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), b'$2b$12$QW/1zgrHumeirkSwiM437u')
    return hashed_password

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Admin Login")  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, "frontend/registration.html", {"form": form})

# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("Admin Login")  # Redirect to the login page after successful registration
#     else:
#         form = UserCreationForm()
#         # Remove field descriptions and error messages
#         for field in form.fields.values():
#             field.help_text = None
#     return render(request, "frontend/registration.html", {"form": form})

# login views for the admin user

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)
            request.session.pop('logged_out', None) # clear logout session variable in login
            return redirect("Dashboard")
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, "frontend/login.html")

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    request.session['logged_out'] = True # Set the session variable to True
    return redirect("Admin Login") # Redirect to the login page after logout
# Create your views here.
# creating views for dashboard

@login_required
def home(request):
    if request.session.get('logged_out', False):
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("login")

    disposed_count = Equipment.objects.filter(current_status ='Disposed').count()
    equipment_count = Equipment.objects.count()
    new_equipment_count =Equipment.objects.filter(current_status ='New').count()
    store_count = Equipment.objects.filter(current_status ='Retrieved').count()
    market_count = Equipment.objects.filter(current_status ='Market').count()
    assigned_to_staff_count = Equipment.objects.filter(current_status ='Assigned to staff').count()
        
    context = {
        'store_count': store_count,
        'equipment_count': equipment_count,
        'new_equipment_count': new_equipment_count,
        'market_count': market_count,
        'disposed_count': disposed_count,
        'assigned_to_staff_count': assigned_to_staff_count,
    }
    return render(request,'frontend/dashboard.html',context)

#All Equipment views
@login_required
def allEquipmentList(request):
    # agencies = Agency.objects.all()
    staffs = Staff.objects.all()
    current_statuses = Equipment._meta.get_field('current_status').choices
    #retrieve all the equipment data from the database
    selected_Equipment =Equipment.objects.values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'purchase_date',
        'purchase_price',
        'supplier',
        'location',
        'delivered_by__name',
        'delivered_date',
        'retrieval_date',
        'retrieved_by',
        'received_by',
        'current_status'
    )
    # Manually setting the initial value for equipment_id
    # for idx, equipment in enumerate(selected_Equipment):
    #     equipment['equipment_id'] = idx + 1

    context = {
      'equipments': selected_Equipment,
    #   'agencies': agencies,
      'current_statuses': current_statuses,
      'staffs': staffs
    }
    #pass the data to template for rendering
    return render(request, 'frontend/student/allequipmentsList.html', context)

@login_required
# @group_required('Admin')
def allEquipmentAdd(request):
    # agencies = Agency.objects.all()
    staffs = Staff.objects.all()
    current_statuses = Equipment._meta.get_field('current_status').choices
    return render(request, 'frontend/student/allequipmentsAdd.html',{'classes': Equipment.objects.all(), 'staffs': staffs, 'current_statuses': current_statuses})

# All equipment registration views
def allEquipmentReg(request):
    if request.method == 'POST':
        equipment_name = request.POST.get('equipment_name')
        brand = request.POST.get('brand')
        serial_number = request.POST.get('serial_number')
        purchase_date_str = request.POST.get('purchase_date', '')
        purchase_price = request.POST.get('purchase_price')
        supplier = request.POST.get('supplier')
        current_status = request.POST.get('current_status')
        received_by = request.POST.get('received_by')
        location = request.POST.get('location')
        retrieved_by =request.POST.get('retrieved_by')
        equipment_condition =request.POST.get('equipment_condition')
        disposal_reason=request.POST.get('disposal_reason')

        
        # Get the Agency object based on the submitted 'agency'
        # agency = get_object_or_404(Agency, agency_name=agency_by_name)
        
        delivered_by_name = request.POST.get('delivered_by')
        
        # Get the Staff object based on the submitted 'delivered_by_name'
        delivered_by = get_object_or_404(Staff, name=delivered_by_name)
        
        # Handle date fields
        delivery_date_str = request.POST.get('delivered_date', '')
        retrieval_date_str = request.POST.get('retrieval_date', '')

        try:
            # Parse date strings to datetime objects (if not empty)
            delivery_date = timezone.datetime.strptime(delivery_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            delivery_date = None

        try:
            retrieval_date = timezone.datetime.strptime(retrieval_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            retrieval_date = None
        
        try:
            purchase_date = timezone.datetime.strptime(purchase_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            purchase_date = None

        try:
            equipment = Equipment.objects.create(
                equipment_name=equipment_name,
                brand=brand,
                serial_number=serial_number,
                purchase_date=purchase_date,
                purchase_price=purchase_price,
                supplier=supplier,
                current_status=current_status,
                received_by =received_by,
                location=location,
                delivered_by=delivered_by,
                delivered_date=delivery_date,
                retrieval_date=retrieval_date,
                retrieved_by=retrieved_by,
                equipment_condition=equipment_condition,
                disposal_reason=disposal_reason
                
            )

            equipment.save()
            messages.success(request, 'Data successfully added!')
            return redirect("addallEquipment")

        except ValidationError as e:
            # Handle validation errors, e.g., display an error message to the user
            messages.error(request, f"Validation error: {e}")
# equipments views
@login_required
def equipmentsList(request):
    #retrieve all the equipment data from the database
    selected_Equipment =Equipment.objects.filter(current_status ='New').values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'purchase_date',
        'purchase_price',
        'supplier',
        'current_status'
    )

    context = {
      'equipments': selected_Equipment
    }
    #pass the data to template for rendering
    return render(request, 'frontend/student/equipmentsList.html', context)

@login_required
def equipmentsAdd(request):
    current_statuses = Equipment._meta.get_field('current_status').choices
    return render(request, 'frontend/student/equipmentsAdd.html',{'classes': Equipment.objects.all(), 'current_statuses': current_statuses})

#equipment registration views
def equipmentReg(request):
    if(request.method == 'POST'):
        equipment_name =request.POST.get('equipment_name')
        brand =request.POST.get('brand')
        serial_number =request.POST.get('serial_number')
        purchase_date =request.POST.get('purchase_date')
        purchase_price =request.POST.get('purchase_price')
        supplier =request.POST.get('supplier')
        current_status = request.POST.get('current_status')

        equipment =Equipment.objects.create(
            equipment_name = equipment_name,            
            brand = brand ,
            serial_number = serial_number ,
            purchase_date=purchase_date,
            purchase_price = purchase_price ,
            supplier = supplier ,
            current_status = current_status
          
        )

        equipment.save ()
        messages.success(request, 'Data successfully added!')
        return redirect("addEquipments")
    
# Delete Equipment
def delete_equipment(request):
    if request.method == "POST":
        equipment_id = request.POST.get("equipment_id")

        equipment = Equipment.objects.get(pk=equipment_id)
        equipment.delete()
        messages.success(request, "Equipment has been deleted")

        return redirect("allEquipmentList")
    
# Edit Equipment
@login_required
def edit_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get("equipment_id")
        equipment_name = request.POST.get('equipment_name')
        brand = request.POST.get('brand')
        serial_number = request.POST.get('serial_number')
        purchase_date_str = request.POST.get('purchase_date', '')
        # purchase_date = request.POST.get('purchase_date')
        purchase_price = request.POST.get('purchase_price')
        supplier = request.POST.get('supplier')
        location = request.POST.get('location')
        delivered_by_name = request.POST.get('delivered_by')
        # delivered_date = request.POST.get('delivered_date')
        # retrieval_date = request.POST.get('retrieval_date')
        delivered_date_str = request.POST.get('delivered_date', '')
        retrieval_date_str = request.POST.get('retrieval_date', '')
        retrieved_by = request.POST.get('retrieved_by')
        current_status = request.POST.get('current_status')

        # Retrieve the equipment instance
        equipment = Equipment.objects.get(pk=equipment_id)
        # Get the Agency object based on the submitted 'agency'
        # agency = get_object_or_404(Agency, agency_name=agency_by_name)
        # Get the Staff object based on the submitted 'delivered_by_name'
        delivered_by = get_object_or_404(Staff, name=delivered_by_name)

        try:
            # Parse date strings to datetime objects (if not empty)
            delivered_date = timezone.datetime.strptime(delivered_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            delivered_date = None

        try:
            retrieval_date = timezone.datetime.strptime(retrieval_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            retrieval_date = None
        
        try:
            purchase_date = timezone.datetime.strptime(purchase_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            purchase_date = None
        try:
            # Update equipment attributes
            equipment.equipment_name = equipment_name
            equipment.brand = brand
            equipment.serial_number = serial_number
            equipment.purchase_date = purchase_date
            equipment.purchase_price = purchase_price
            equipment.supplier = supplier
            equipment.location = location
            equipment.delivered_by = delivered_by
            equipment.delivered_date = delivered_date
            equipment.retrieval_date = retrieval_date
            equipment.retrieved_by = retrieved_by
            equipment.current_status = current_status

            # Save the updated equipment
            equipment.save()

            messages.success(request, "Equipment edited successfully")
            return redirect("allEquipmentList")
        except ValidationError as e:
            # Handle validation errors, e.g., display an error message to the user
            messages.error(request, f"Validation error: {e}")


#Equipment Assigned to staff
@login_required
def staffEquipment(request):
    #retrieve all the equipment data from the database
    selected_Equipment =Equipment.objects.filter(current_status ='Assigned to staff').values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'delivered_date',
        'delivered_by__name',
        'current_status'
    )

    context = {
      'equipments': selected_Equipment
    } 
    #pass the data to template for rendering
    return render(request, 'frontend/student/assignedToStaff.html', context)
    

#Market views
@login_required
def teacherAdd(request):
    classes = Schoolclasses.objects.all()
    subjects = Subjects.objects.all()
    return render(request,'frontend/staff/teacherAdd.html', {'classes': classes, 'subjects':subjects})

@login_required
def marketList(request):
    marketEquipment = Equipment.objects.filter(current_status ='Market').values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'location',
        'delivered_date',
        'delivered_by__name'

    )

    context = {
      'marketEquipment': marketEquipment
    }
    return render(request,'frontend/student/marketequipment.html', context)

#STORE EQUIPMENT
@login_required
def retrievedList(request):
    storeEquipment =Equipment.objects.filter(current_status ='Retrieved').values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'location',
        'equipment_condition',
    )

    context = {
      'stores': storeEquipment
    }
    return render(request,'frontend/student/store.html', context)

#Disposed Equipment
@login_required
def disposedEquipment(request):
    disposedEquipment =Equipment.objects.filter(current_status='Disposed').values(
        'equipment_id',
        'equipment_name',
        'brand',
        'serial_number',
        'disposal_reason',
    )

    context = {
      'disposals': disposedEquipment
    }
    return render(request,'frontend/student/disposedComputers.html', context)

# Agency Views
@login_required
def agencyAdd(request):
    agencies = Agency.objects.all()
    return render(request,'frontend/student/agencyadd.html', {'agencies': agencies})

# Agency Registration
@login_required
def agencyReg(request):
    if(request.method == 'POST'):
        agency_name =request.POST.get('agency_name')
        pcc =request.POST.get('pcc')

        agency =Agency.objects.create(
            agency_name = agency_name,            
            pcc = pcc           
        )

        agency.save ()
        messages.success(request, 'Data successfully added!')
        return redirect("AddAgency")
    
# Agency list
@login_required
def agencyList(request):
    agency =Agency.objects.values(
        'agency_id',
        'agency_name',
        'pcc'
    )

    context = {
      'agencies': agency
    }
    return render(request,'frontend/student/agencylist.html', context)
# Staff Views
@login_required
def staffAdd(request):
    staff = Staff.objects.all()
    departments = Staff._meta.get_field('department').choices
    return render(request,'frontend/student/staffadd.html', {'staffs': staff, 'departments':departments})

# staff Registration
@login_required
def staffReg(request):
    if(request.method == 'POST'):
        name =request.POST.get('name')
        department =request.POST.get('department')

        staff =Staff.objects.create(
            name = name,            
            department = department           
        )

        staff.save ()
        messages.success(request, 'Data successfully added!')
        return redirect("AddStaff")
    
# Staff list
@login_required
def staffList(request):
    staff =Staff.objects.values(
        'staff_id',
        'name',
        'department'
    )

    context = {
      'staffs': staff
    }
    return render(request,'frontend/student/stafflist.html', context)

# Delete Staff
def delete_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff = Staff.objects.get(pk=staff_id)
        staff.delete()
        messages.success(request, "Staff has been deleted")
        return redirect("ListStaff")
# edit staff
@login_required
def edit_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        name = request.POST.get('name')
        department = request.POST.get('department')

        # Retrieve staff
        staff = Staff.objects.get(pk=staff_id)     

        try:
            staff.name = name
            staff.department =department
            staff.save()
            messages.success(request, 'Data successfully edited!')
            return redirect("ListStaff")

        except ValidationError as e:
            # Handle validation errors, e.g., display an error message to the user
            messages.error(request, f"Validation error: {e}")
            return redirect("ListStaff")
# Asset views
@login_required
def assetAdd(request):
    return render(request, 'frontend/student/asset.html')

#Asset Registration
def assetReg(request):
    if request.method == 'POST':
        asset_name = request.POST.get('asset_name')
        brand = request.POST.get('brand')
        serial_number = request.POST.get('serial_number')
        aquisition_cost =request.POST.get('aquisition_cost')
        aquisition_date_str = request.POST.get('aquisition_date', '')
        location = request.POST.get('location')
        delivery_date_str = request.POST.get('delivery_date')
        delivered_by = request.POST.get('delivered_by')
        
        # Handle date fields
        try:
            aquisition_date = timezone.datetime.strptime(aquisition_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            aquisition_date = None

        try:
            # Parse date strings to datetime objects (if not empty)
            delivery_date = timezone.datetime.strptime(delivery_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            delivery_date = None

        try:
            asset = Asset.objects.create(
                asset_name=asset_name,
                brand=brand,
                serial_number=serial_number,
                aquisition_cost=aquisition_cost,
                aquisition_date =aquisition_date,
                location=location,
                delivery_date=delivery_date,
                delivered_by=delivered_by
            )

            asset.save()
            messages.success(request, 'Data successfully added!')
            return redirect("addAsset")

        except ValidationError as e:
            # Handle validation errors, e.g., display an error message to the user
            messages.error(request, f"Validation error: {e}")
#Asset list
@login_required
def assetList(request):
    #retrieve all the asset data from the database
    selected_asset =Asset.objects.values(
        'asset_id',
        'asset_name',
        'brand',
        'serial_number',
        'aquisition_cost',
        'aquisition_date',
        'location',
        'delivery_date',
        'delivered_by'
    )

    context = {
      'assets': selected_asset
    }
    #pass the data to template for rendering
    return render(request, 'frontend/student/assetlist.html', context)

#delete asset
def delete_asset(request):
    if request.method == "POST":
        asset_id = request.POST.get("asset_id")
        asset = Asset.objects.get(pk=asset_id)
        asset.delete()
        messages.success(request, "Asset has been deleted")

        return redirect("AssetList")
    
# edit asset
@login_required
def edit_asset(request):
    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        asset_name = request.POST.get('asset_name')
        brand = request.POST.get('brand')
        serial_number = request.POST.get('serial_number')
        aquisition_cost = request.POST.get('aquisition_cost')
        aquisition_date_str = request.POST.get('aquisition_date', '')
        location = request.POST.get('location')
        delivery_date_str = request.POST.get('delivery_date')
        delivered_by = request.POST.get('delivered_by')
        
        # Retrieve asset 
        asset = Asset.objects.get(pk=asset_id)
        
        # Handle date fields
        try:
            aquisition_date = timezone.datetime.strptime(aquisition_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            aquisition_date = None

        try:
            # Parse date strings to datetime objects (if not empty)
            delivery_date = timezone.datetime.strptime(delivery_date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            delivery_date = None       

        try:
            asset.asset_name = asset_name
            asset.brand = brand
            asset.serial_number = serial_number
            asset.aquisition_cost = aquisition_cost
            asset.aquisition_date = aquisition_date
            asset.location = location
            asset.delivery_date = delivery_date
            asset.delivered_by = delivered_by

            asset.save()
            messages.success(request, 'Data successfully edited!')
            return redirect("AssetList")

        except ValidationError as e:
            # Handle validation errors, e.g., display an error message to the user
            messages.error(request, f"Validation error: {e}")
            return redirect("AssetList")
    
        return render(request, 'frontend/student/studentsList.html', {'error_message': str(e)})

# users views
@login_required
def addUsers(request):
    return render(request,'frontend/users/addUsers.html')

@login_required
def usersList(request):
    return render(request,'frontend/users/usersList.html')


# import Equipment
from django.db.models import Q  # Import Q for complex queries

def import_equipment(request):
    if request.method == 'POST':
        equipment_file = request.FILES.get('equipment_file')

        if equipment_file:
            try:
                equipment_data = pd.read_excel(equipment_file)

                for index, row in equipment_data.iterrows():

                    # Check for empty values before assigning
                    equipment_name = row['equipment_name'] if not pd.isnull(row['equipment_name']) else None
                    brand = row['brand'] if not pd.isnull(row['brand']) else None
                    serial_number = row['serial_number'] if not pd.isnull(row['serial_number']) else None
                    delivered_by_name = row['delivered_by'] if not pd.isnull(row['delivered_by']) else None
                    retrieved_by = row['retrieved_by'] if not pd.isnull(row['retrieved_by']) else None
                    delivered_date = row['delivered_date'] if not pd.isnull(row['delivered_date']) else None
                    retrieval_date = row['retrieval_date'] if not pd.isnull(row['retrieval_date']) else None
                    purchase_date = row['purchase_date'] if not pd.isnull(row['purchase_date']) else None
                    location = row['location'] if not pd.isnull(row['location']) else None
                    purchase_price = row['purchase_price'] if not pd.isnull(row['purchase_price']) else None
                    received_by = row['received_by'] if not pd.isnull(row['received_by']) else None
                    supplier = row['supplier'] if not pd.isnull(row['supplier']) else None
                    current_status = row['current_status'] if not pd.isnull(row['current_status']) else None

                    # Retrieve the Staff object if delivered_by_name is not empty
                    delivered_by = None
                    if delivered_by_name:
                        delivered_by = Staff.objects.get_or_create(name=delivered_by_name)[0]

                    # Create the Equipment object only if equipment_name is not empty
                    if equipment_name is not None:
                        Equipment.objects.create(
                            equipment_name=equipment_name,
                            brand=brand,
                            serial_number=serial_number,
                            delivered_by=delivered_by,
                            retrieved_by=retrieved_by,
                            delivered_date=delivered_date,
                            retrieval_date=retrieval_date,
                            purchase_date=purchase_date,
                            location=location,
                            purchase_price=purchase_price,
                            received_by=received_by,
                            supplier=supplier,
                            current_status=current_status
                        )

                messages.success(request, "Equipment imported successfully.")
                return redirect('addallEquipment')

            except Exception as e:
                messages.error(request, f"Error importing equipment: {str(e)}")
                return redirect('addallEquipment')

    return redirect('addallEquipment')


def export_equipment_to_excel(request):
    try:
        equipment = Equipment.objects.all()

        # Create a new workbook and add a worksheet
        wb = openpyxl.Workbook()
        ws = wb.active

        # Write headers to the worksheet
        headers = [
            'Equipment ID', 'Equipment Name', 'Brand', 'Serial Number', 'Location', 'Delivered By', 
            'Retrieved By', 'Delivered Date', 'Retrieval Date', 'Purchase Date', 
            'Purchase Price', 'Received By', 'Supplier', 'Current Status'
        ]
        ws.append(headers)

        # Write equipment data to the worksheet
        for idx, equip in enumerate(equipment, start=1):
            ws.append([
                idx, equip.equipment_name, equip.brand, equip.serial_number, 
                equip.location, equip.delivered_by.name if equip.delivered_by else '', 
                equip.retrieved_by, equip.delivered_date, equip.retrieval_date, 
                equip.purchase_date, equip.purchase_price, 
                equip.received_by, equip.supplier, equip.current_status
            ])

        # Set column widths for all columns
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width

        # Create an HttpResponse with the Excel file
        filename = 'equipment_data.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Save the workbook to the response
        wb.save(response)
        messages.success(request, 'Equipment data successfully exported to Excel.')
        return response

    except Equipment.DoesNotExist:
        return HttpResponse('Equipment not found', status=404)


# settings views
@login_required
def settings(request):
    if request.method == "POST":
        current_term = request.POST.get("term")
        current_year = request.POST.get("year")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Check if the end_date of the previous term has been reached
        # previous_term = Term.objects.filter(status=1).first()
        # if previous_term and date.today() < previous_term.end_date:
        #     messages.error(request, "Cannot add a new term before the current term ends.")
        #     return redirect("settings")

        # First, set the status of any existing terms to expired
        # Term.objects.update(status=0)
        
        # Create a new Term object and set its status to current
        # new_term = Term.objects.create(
        #     current_term=current_term,
        #     current_year=current_year,
        #     start_date=start_date,
        #     end_date=end_date,
        #     status=1  # Set as current term
        # )
        messages.success(request, "New term settings have been added successfully")

        return redirect("settings")
    
    context = {
        # 'term_data' : Term.objects.filter(status=1)
    }
    return render(request, "frontend/settings.html", context)

# edit term
def edit_term(request):
    if request.method == "POST":
        id = request.POST.get("id")
        term = request.POST.get("term")
        # year = request.POST.get("year")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        this_term = Term.objects.get(id=id)

        this_term.current_term = term
        # this_term.current_year = year
        this_term.start_date = start_date
        this_term.end_date = end_date

        this_term.save()
        messages.success(request, "Academic term edit successfully")
        return redirect("settings")

# delete term
def delete_term(request):
    if request.method == "POST":
        id = request.POST.get("id")
        # this_term = Term.objects.get(id=id)

        # this_term.delete()
        messages.success(request, "Academic term deleted successfully")
        return redirect("settings")


# school information
@login_required
def school_info(request):
    if request.method == "POST":
        badge = request.FILES.get('badge')
        schoolname = request.POST.get("schoolname")
        contact = request.POST.get("contact")
        box_number = request.POST.get("box_number")
        email = request.POST.get("email")
        website = request.POST.get("website")

        # Check if there's existing school info data, assuming only one instance
        school_info = SchoolInfo.objects.first()

        if school_info is None:
            # If no data exists, create a new instance
            school_info = SchoolInfo(
                schoolname=schoolname,
                contact=contact,
                box_number=box_number,
                email=email,
                website=website,
            )
        else:
            # If data exists, update it
            messages.success(request, 'You can only add this information once!')
            return redirect("School Information")  

        if badge:
            fs = FileSystemStorage()
            image_filename = fs.save(badge.name, badge)
            school_info.badge = image_filename

        school_info.save()
        messages.success(request, 'School information updated successfully!')
        return redirect("School Information")  # Use the appropriate URL name for school_info page
    
    context = {
        'school_data': SchoolInfo.objects.all()
    }
    return render(request, "frontend/school_info.html", context)

def edit_school_info(request):
    if request.method == "POST":
        school_id = request.POST.get("id")
        school = get_object_or_404(SchoolInfo, pk=school_id)

        # Update school information based on form data
        school.schoolname = request.POST.get("schoolname")
        school.contact = request.POST.get("contact")
        school.box_number = request.POST.get("box_number")
        school.email = request.POST.get("email")
        school.website = request.POST.get("website")

        # Handle badge image update if necessary
        badge = request.FILES.get('badge')
        if badge:
            school.badge = badge

        school.save()

        # Add success message
        messages.success(request, 'School information updated successfully!')
        return redirect("School Information")

    # Render the school information template with context
    context = {
        'school_data': SchoolInfo.objects.all()
    }
    return render(request, "frontend/school_info.html", context)

# Fetch the groups function
# def my_view(request):
#     groups = Group.objects.all()  # Fetch all groups from the database
#     print(groups)
#     return render(request, 'settings.html', {'groups': groups})
    
# create user
def create_user(request):
    groups = Group.objects.all()  # Fetch all groups from the database
    print(f"Groups: {groups}") 
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        group_id = request.POST.get('group')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('create_user')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('create_user')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.full_name = full_name
        user.save()

        #Add user to the selected group
        try:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
        except Group.DoesNotExist:
            messages.error(request, 'Invalid group selected.')
            return redirect('create_user')

        messages.success(request, f'User {username} created successfully!')
        # return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'frontend/settings.html', {'groups': groups})

def display_users(request):
    # Retrieve user objects
    users = User.objects.all()
    user_data = []
    for user in users:
        # Retrieve groups associated with the user
        groups = user.groups.all().values_list('name', flat=True)
        group_names = list(groups) 
        user_info = {
            'username': user.username,
            # 'full_name': user.get_full_name(),
            'email': user.email,
            'last_login': user.last_login,
            'groups': group_names
        }
        user_data.append(user_info)

    # Render the template with user data
    return render(request, 'frontend/users.html', {'user_data': user_data})

# edit user
def edit_user_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Retrieve the user object to update
        user = User.objects.get(id=user_id)

        # Update user information
        user.full_name = full_name
        user.username = username
        user.email = email
        user.save()

        # return redirect('user_profile')

# other users views
@login_required
def create_other_users(request):
    otherusers = OtherUsers.objects.all()
    return render(request,'frontend/addotherusers.html', {'otherusers': otherusers})

@login_required
def otherUsersReg(request):
    if(request.method == 'POST'):
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        otheruser =OtherUsers.objects.create(
            full_name=full_name, 
            username=username, 
            email=email, 
            password=password        
        )

        otheruser.save ()
        messages.success(request, 'User successfully added!')
        return redirect("create_other_users")
    

# def otherUsersReg(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('full_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Check if username or email already exists
#         if OtherUsers.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return redirect('create_user')
#         if OtherUsers.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists.')
#             return redirect('create_user')

#         # Create the OtherUsers object and save it
#         otheruser = OtherUsers.objects.create(full_name=full_name, username=username, email=email, password=password)
#         otheruser.save()

#         messages.success(request, f'User {username} created successfully!')
#         # Redirect to a success page or login page
#         return redirect('create_other_users')  # Assuming 'create_user' is the URL name for the page where users are created

#     return render(request, 'frontend/addotherusers.html')



