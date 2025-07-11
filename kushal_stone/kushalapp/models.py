from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
        ('Manager', 'Manager'),
        ('Finance', 'Finance')
    ]
    
    mobile_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Add related_name to prevent clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique reverse relation for CustomUser
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique reverse relation for CustomUser
        blank=True
    )
    
    # class Meta:
    #     unique_together = ('mobile_number', 'role')  # Ensure unique combination of mobile_number and role


class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




from django.db import models

class QuotationTerm(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

class InvoiceTerm(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Lead(models.Model):
    CUSTOMER_SEGMENT_CHOICES = [
        ('Retail/individual', 'Retail/individual'),
        ('B2B', 'B2B'),
        ('Reseller', 'Reseller'),
        ('Commercial/Corporate', 'Commercial/Corporate')
    ]

    SOURCE_CHOICES = [
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Indiamart', 'Indiamart'),
        ('Google', 'Google'),
        ('Reference', 'Reference'),
        ('Other', 'Other')
    ]

    LEAD_TYPE_CHOICES = [
        ('Hot', 'Hot'),
        ('Warm', 'Warm'),
        ('Cold', 'Cold'),
        ('Not Interested', 'Not Interested'),
        ('Irrelevant', 'Irrelevant'),
    ]

    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    status = models.CharField(max_length=20, blank=True, null=True) 
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=25)
    secondary_mobile_number = models.CharField(max_length=25, blank=True, null=True)  # <-- Add this

    email = models.EmailField(blank=True, null=True)
    requirements = models.CharField(max_length=50)
    products = models.ManyToManyField('Product', blank=True)
    services = models.ManyToManyField('Service', blank=True)
    address = models.TextField()
    architect_name = models.CharField(max_length=100, blank=True, null=True)
    architect_number = models.CharField(max_length=15, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    source_other = models.CharField(max_length=100, blank=True, null=True)
    enquiry_date = models.DateField()
    sales_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sales_person')
    customer_segment = models.CharField(max_length=50, choices=CUSTOMER_SEGMENT_CHOICES)
    next_followup_date = models.DateField(null=True, blank=True)
    follow_up_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='follow_up_person',blank=True)
    is_closed = models.BooleanField(default=False)
    win_status = models.BooleanField(null=True, blank=True)
    closed_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='closed_leads')
    assigned_to_operations = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_operations_leads')

    # New Fields
    first_call_date = models.DateField(null=True, blank=True)
    customer_visited = models.CharField(max_length=10, choices=YES_NO_CHOICES, null=True, blank=True)
    inspection_done = models.CharField(max_length=10, choices=YES_NO_CHOICES, null=True, blank=True)
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES, null=True, blank=True)
    quotation_given = models.CharField(max_length=10, choices=YES_NO_CHOICES, null=True, blank=True)
    quotation_amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file_upload = models.FileField(upload_to='lead_files/', null=True, blank=True)

    def __str__(self):
        return self.full_name

from django.utils import timezone


class FollowUpBase(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    LEAD_TYPE_CHOICES = [
        ('Hot', 'Hot'),
        ('Warm', 'Warm'),
        ('Cold', 'Cold'),
        ('Not Interested', 'Not Interested')
    ]

    followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES)
    remarks = models.TextField()
    close_status = models.CharField(
        max_length=10,
        choices=[('Open', 'Open'), ('Win', 'Win'), ('Loss', 'Loss')],
        default='Open',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        abstract = True

class FollowUp1(FollowUpBase):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    customer_visited = models.BooleanField()
    inspection_done = models.BooleanField()
    quotation_given = models.BooleanField()
    quotation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    quotation_file = models.FileField(upload_to='quotations/', null=True, blank=True)
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup2_person',blank=True,)


class FollowUp2(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup3_person')

class FollowUp3(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup4_person')


class FollowUp4(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup5_person')


class FollowUp5(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup6_person')


class FollowUp6(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup7_person')


class FollowUp7(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup8_person')


class FollowUp8(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup9_person')


class FollowUp9(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup10_person')


class FollowUp10(FollowUpBase):
    # No next follow-up
    pass


# start

class Quotation(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    services = models.ManyToManyField('Service', blank=True)
    products = models.ManyToManyField('Product', blank=True)

    # actual_price=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # quantity = models.PositiveIntegerField(null=True, blank=True)
    # gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # terms_and_conditions = models.ManyToManyField('QuotationTerm', blank=True)

    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_with_gst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    enable_gst = models.BooleanField(default=False)

    def __str__(self):
        return f"Quotation for {self.full_name}"


    
class QuotationProduct(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2)

class QuotationService(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2)


    
