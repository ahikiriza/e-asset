from django.db import models
from django.contrib.auth.models import User

# Asset models

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    # department = models.CharField(max_length=255, default=None)
    department = models.CharField(max_length=50, choices=[
        ('Technical', 'Technical'),
        ('Sales & Marketing', 'Sales & Marketing'),
        ('HelpDesk', 'HelpDesk'),
        ('Finance', 'Finance'),
        ('Admin', 'Admin'),
    ])
    Display_Staff = [
        'staff_id', 'name', 'department'
    ]

class Agency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=255, unique=True)
    pcc = models.CharField(max_length=255)
    Display_Agency = [
        'agency_id', 'agency_name', 'pcc'
    ]

class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True , default= None)
    serial_number = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    delivered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    retrieved_by = models.CharField(max_length=255, null=True, blank=True)
    delivered_date = models.DateField( null=True, blank=True)
    retrieval_date = models.DateField( null=True, blank=True)
    purchase_date = models.DateField( null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received_by = models.CharField(max_length=255, null=True, blank=True)
    supplier = models.CharField(max_length=255, blank=True , default= None, null=True)
    equipment_condition = models.CharField(max_length=255, null=True, blank=True)
    disposal_reason = models.CharField(max_length=255, null=True, blank=True)
    current_status = models.CharField(max_length=50, choices=[
        ('Retrieved', 'Retrieved'),
        ('Market', 'Market'),
        ('Assigned to staff', 'Assigned to staff'),
        ('Disposed', 'Disposed'),
        ('New', 'New'),
    ])
    disposed_by = models.ManyToManyField(Staff, related_name='disposed_equipment', blank=True)

    Display_Equipment = [
        'equipment_id', 'equipment_name', 'brand', 'serial_number', 'agency','delivered_by', 'delivered_date', 'retrieval_date', 'purchase_date', 'location', 'purchase_price',
        'supplier','received_by', 'equipment_condition', 'disposal_reason', 'current_status'
    ]

class MarketTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Equipment")
    transaction_type = models.CharField(max_length=50, choices=[
        ('Bought', 'Bought'),
        ('Taken to market', 'Taken to market'),
        ('Retrieved from market', 'Retrieved from market'),
        ('Assigned to staff', 'Assigned to staff'),
    ])
    transaction_date = models.DateTimeField(null=True, blank= True)
    transaction_details = models.TextField(blank=True , default= None)
    recipient_type = models.CharField(max_length=50, choices=[
        ('Market', 'Market'),
        ('Staff', 'Staff'),
        ('Disposal', 'Disposal'),
    ])

    Display_MarketTransaction = [
        'transaction_id', 'equipment', 'transaction_type', 'transaction_date', 'transaction_details', 'recipient_type'
    ]

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name ="Equipment")
    storage_condition = models.CharField(max_length=50, choices=[
        ('Good', 'Good'),
        ('Needs repair', 'Needs repair'),
        ('Disposed', 'Disposed'),
    ])

    Display_Store = [
        'store_id', 'equipment', 'storage_condition'
    ]

class DisposedComputer(models.Model):
    disposed_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    disposal_date = models.DateTimeField(null=True, blank =True)
    disposal_reason = models.CharField(max_length=255, blank=True , default= None)
    disposal_details = models.TextField(blank=True , default= None)

    Display_DisposedComputer = [
        'disposed_id', 'equipment', 'disposal_date', 'disposal_reason', 'disposal_details'
    ]

class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=255)
    brand =models.CharField(max_length =255, blank=True)
    serial_number =models.CharField(max_length =50)
    aquisition_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aquisition_date = models.DateField(null=True, blank =True)
    location = models.CharField(max_length=255, blank=True , default= None)
    delivery_date = models.DateField(null=True, blank =True)
    delivered_by = models.CharField(max_length=255, blank =True)

    Display_Asset = [
        'asset_id', 'asset_name', 'brand', 'serial_number', 'aquisition_cost','aquisition_date','location','delivery_date','delivered_by'
    ]

#login model
class Login(models.Model):
    username = models.CharField(max_length=25, blank=True, verbose_name="Username")
    email = models.EmailField(max_length=254, default=None, verbose_name="Email")
    password = models.CharField(max_length=255, verbose_name='Enter the password')
    
    Display_Login_Fields = ['username','email','password']
 #user roles model
class Role_Model(models.Model):
    # id =models.CharField(max_length=10, verbose_name='Role ID')
    rolename = models.CharField(max_length=255, verbose_name='Role Name')
    Display_Roles = ['rolename']    

# Other users model
class OtherUsers(models.Model):
    id = models.AutoField(primary_key=True)
    full_name =models.CharField(max_length=255, blank=True, verbose_name="Full Name")
    username = models.CharField(max_length=25, blank=True, verbose_name="Username")
    email = models.EmailField(max_length=254, default=None, verbose_name="Email")
    password = models.CharField(max_length=255, verbose_name='Enter the password')
    
    Display_Login_Fields = ['full_name','username','email','password']
    
# Event logging in django
class Event(models.Model):
    EVENT_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('access', 'Access'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"} {self.event_type} {self.path} at {self.timestamp}'

    
    