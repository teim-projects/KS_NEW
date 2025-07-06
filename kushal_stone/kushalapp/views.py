from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')



from django.http import JsonResponse
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.GET.get('username')
        email = request.GET.get('email')
        response = {}

        if username and CustomUser.objects.filter(username=username).exists():
            response['username_error'] = "Username already exists"

        if email and CustomUser.objects.filter(email=email).exists():
            response['email_error'] = "Email already registered"

        return JsonResponse(response)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        CustomUser.objects.create_user(username=username, email=email, password=password, role='Admin')
        messages.success(request, 'Admin registered successfully')
        return redirect('login')

    return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()  # Ensure you are using the correct user model

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomUser  # Import your custom user model

def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']  # Form field still named 'username'
        password = request.POST['password']

        print(f"Attempting login: Email={email}, Password={password}")  # Debugging

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email does not exist.')
            return render(request, 'login.html')

        # Now check password
        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth:
            print(f"Authenticated User: {user_auth.username} - {user_auth.role}")  # Debugging
            login(request, user_auth)
            role = user_auth.role.lower()
            return redirect(reverse(f'{role}_dashboard'))
        else:
            messages.error(request, 'Incorrect password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')



from django.shortcuts import render, redirect, get_object_or_404
from .models import QuotationTerm, InvoiceTerm

# --- QUOTATION TERMS ---

def quotation_term_list(request):
    terms = QuotationTerm.objects.all()
    return render(request, 'quotation_term_view.html', {'terms': terms})

def add_quotation_term(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            QuotationTerm.objects.create(description=description)
        return redirect('quotation_term_list')
    return render(request, 'quotation_term_add.html')

def edit_quotation_term(request, pk):
    term = get_object_or_404(QuotationTerm, pk=pk)
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            term.description = description
            term.save()
        return redirect('quotation_term_list')
    return render(request, 'quotation_term_edit.html', {'term': term})

def delete_quotation_term(request, pk):
    term = get_object_or_404(QuotationTerm, pk=pk)
    term.delete()
    return redirect('quotation_term_list')

# --- INVOICE TERMS ---

def invoice_term_list(request):
    terms = InvoiceTerm.objects.all()
    return render(request, 'invoice_term_view.html', {'terms': terms})

def add_invoice_term(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            InvoiceTerm.objects.create(description=description)
        return redirect('invoice_term_list')
    return render(request, 'invoice_term_add.html')

def edit_invoice_term(request, pk):
    term = get_object_or_404(InvoiceTerm, pk=pk)
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            term.description = description
            term.save()
        return redirect('invoice_term_list')
    return render(request, 'invoice_term_edit.html', {'term': term})

def delete_invoice_term(request, pk):
    term = get_object_or_404(InvoiceTerm, pk=pk)
    term.delete()
    return redirect('invoice_term_list')




# def get_latest_followup_type(lead):
#     for model in [FollowUp10, FollowUp9, FollowUp8, FollowUp7, FollowUp6, FollowUp5, FollowUp4, FollowUp3, FollowUp2, FollowUp1]:
#         followup = model.objects.filter(lead=lead).first()
#         if followup:
#             return followup.lead_type, followup.close_status
#     return None, None




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Lead
from .models import (
    FollowUp1, FollowUp2, FollowUp3, FollowUp4,
    FollowUp5, FollowUp6, FollowUp7, FollowUp8,
    FollowUp9, FollowUp10, FollowUpBase
)

@login_required
def sales_dashboard(request):
    total_leads = Lead.objects.count()
    completed_leads = Lead.objects.filter(is_closed=True).count()
    my_work_total = Lead.objects.filter(sales_person=request.user).count()

    # Get selected follow-up model if required
    follow_up_type = request.GET.get('follow_up_type', 'FollowUp1')
    follow_up_model = globals().get(follow_up_type, FollowUp1)

    # Lead Type chart
    lead_types = Lead.objects.exclude(lead_type__isnull=True).exclude(lead_type='') \
    .values('lead_type').annotate(count=Count('lead_type'))

    lead_type_labels = [entry['lead_type'] for entry in lead_types]
    lead_type_counts = [entry['count'] for entry in lead_types]


    print("Lead Type Labels:", lead_type_labels)
    print("Lead Type Counts:", lead_type_counts)


    # Win/Loss
    win_loss = Lead.objects.filter(is_closed=True).values('win_status').annotate(count=Count('win_status'))
    win_loss_labels = ['Win' if entry['win_status'] else 'Loss' for entry in win_loss]
    win_loss_counts = [entry['count'] for entry in win_loss]

    # Customer Segment
    customer_segments = Lead.objects.values('customer_segment').annotate(count=Count('customer_segment'))
    customer_segment_labels = [entry['customer_segment'] for entry in customer_segments]
    customer_segment_counts = [entry['count'] for entry in customer_segments]

    # Lead Source
    sources = Lead.objects.values('source').annotate(count=Count('source'))
    source_labels = [entry['source'] for entry in sources]
    source_counts = [entry['count'] for entry in sources]

    context = {
        'total_leads': total_leads,
        'completed_leads': completed_leads,
        'my_work_total': my_work_total,
        'lead_type_labels': lead_type_labels,
        'lead_type_counts': lead_type_counts,
        'win_loss_labels': win_loss_labels,
        'win_loss_counts': win_loss_counts,
        'customer_segment_labels': customer_segment_labels,
        'customer_segment_counts': customer_segment_counts,
        'source_labels': source_labels,
        'source_counts': source_counts,
        'follow_up_type': follow_up_type
    }

    return render(request, 'sales_dashboard.html', context)






@login_required
def operations_dashboard(request):
    return render(request, 'operations_dashboard.html')

@login_required
def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')

@login_required
def finance_dashboard(request):
    return render(request, 'finance_dashboard.html')

from django.contrib.auth import get_user_model
CustomUser = get_user_model()




from django.http import JsonResponse

def create_user(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.GET.get('email')
        mobile = request.GET.get('mobile')
        role = request.GET.get('role')

        response = {}

        if email and CustomUser.objects.filter(email=email).exists():
            response['email_error'] = 'Email already exists'

        if mobile and role and CustomUser.objects.filter(mobile_number=mobile, role=role).exists():
            response['mobile_error'] = 'User with this mobile number and role already exists'

        return JsonResponse(response)

    # Standard POST handling
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('create_user')

        if CustomUser.objects.filter(mobile_number=mobile, role=role).exists():
            messages.error(request, 'User with this mobile number and role already exists')
            return redirect('create_user')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('create_user')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            mobile_number=mobile,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, 'User created successfully')
        return redirect('admin_dashboard')

    return render(request, 'create_user.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser

def view_users(request):
    users = CustomUser.objects.all()
    return render(request, 'view_users.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = user.email  # keep username in sync
        user.mobile_number = request.POST.get('mobile')
        user.role = request.POST.get('role')

        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, 'User updated successfully')
        return redirect('view_users')

    return render(request, 'edit_user.html', {'user': user})

def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('view_users')
    return redirect('view_users')






from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Service

def is_admin_user(user):
    return user.is_authenticated and user.role == 'Admin'

@login_required
@user_passes_test(is_admin_user)
def requirements_dashboard(request):
    products = Product.objects.all()
    services = Service.objects.all()

    if request.method == 'POST':
        if 'add_product' in request.POST:
            name = request.POST.get('product_name')
            if name:
                Product.objects.create(name=name)
                messages.success(request, 'Product added successfully.')
                return redirect('requirements_dashboard')

        elif 'add_service' in request.POST:
            name = request.POST.get('service_name')
            if name:
                Service.objects.create(name=name)
                messages.success(request, 'Service added successfully.')
                return redirect('requirements_dashboard')

    return render(request, 'requirements_dashboard.html', {
        'products': products,
        'services': services,
    })
@login_required
@user_passes_test(is_admin_user)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('requirements_dashboard')

@login_required
@user_passes_test(is_admin_user)
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('requirements_dashboard')

@login_required
@user_passes_test(is_admin_user)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('product_name')
        if new_name:
            product.name = new_name
            product.save()
            return redirect('requirements_dashboard')
    return render(request, 'edit_product.html', {'product': product})

@login_required
@user_passes_test(is_admin_user)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('service_name')
        if new_name:
            service.name = new_name
            service.save()
            return redirect('requirements_dashboard')
    return render(request, 'edit_service.html', {'service': service})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Service, Lead, CustomUser

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lead, Product, Service, CustomUser

@login_required
def add_lead(request):
    products = Product.objects.all()
    services = Service.objects.all()
    sales_persons = CustomUser.objects.filter(role='Sales')
    follow_up_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        errors = {}

        close_lead = data.get('close_lead')  # Checkbox
        win_status = data.get('win_status')

        status = None
        is_closed = False  # Default: not closed

        if close_lead == 'on':
            is_closed = True
            if win_status == 'win':
                status = 'Win'
            elif win_status == 'loss':
                status = 'Loss'
            else:
                errors['win_status'] = "Please select Win or Loss."
        else:
            # Only required when not closing the lead
            if not data.get('next_followup_date'):
                errors['next_followup_date'] = "This field can't be empty."
            if not data.get('follow_up_person'):
                errors['follow_up_person'] = "This field can't be empty."

        required_fields = [
            'full_name', 'mobile_number', 'mobile_country_code', 'requirements',
            'address', 'source', 'enquiry_date', 'sales_person', 'customer_segment'
        ]

        for field in required_fields:
            if not data.get(field):
                errors[field] = "This field can't be empty."

        if data.get('source') == 'Other' and not data.get('source_other'):
            errors['source_other'] = "Please specify other source."

        if data.get('quotation_given') == 'Yes' and not data.get('quotation_amount'):
            errors['quotation_amount'] = "Enter the quotation amount."

        if errors:
            return render(request, 'add_lead.html', {
                'products': products,
                'services': services,
                'sales_persons': sales_persons,
                'follow_up_persons': follow_up_persons,
                'errors': errors,
                'data': data,
                'country_codes': [('+91', '🇮🇳 India')],
            })

        # Construct full mobile numbers
        mobile_number = f"{data.get('mobile_country_code')} {data.get('mobile_number')}"
        secondary_mobile_number = (
            f"{data.get('secondary_country_code')} {data.get('secondary_mobile_number')}"
            if data.get('secondary_mobile_number') else None
        )

        lead = Lead.objects.create(
            full_name=data['full_name'],
            mobile_number=mobile_number,
            secondary_mobile_number=secondary_mobile_number,
            email=data.get('email'),
            requirements=data['requirements'],
            address=data['address'],
            architect_name=data.get('architect_name'),
            architect_number=data.get('architect_number'),
            source=data['source'],
            source_other=data.get('source_other'),
            enquiry_date=data['enquiry_date'],
            sales_person_id=data['sales_person'],
            customer_segment=data['customer_segment'],
            next_followup_date=None if close_lead == 'on' else data.get('next_followup_date'),
            follow_up_person_id=None if close_lead == 'on' else data.get('follow_up_person'),
            first_call_date=data.get('first_call_date') or None,
            customer_visited=data.get('customer_visited'),
            inspection_done=data.get('inspection_done'),
            lead_type=data.get('lead_type'),
            quotation_given=data.get('quotation_given'),
            quotation_amount=data.get('quotation_amount') or None,
            description=data.get('description'),
            file_upload=files.get('file_upload'),
            status=status,
            is_closed=is_closed,
        )

        # Handle many-to-many for products/services
        if data['requirements'] == 'products':
            lead.products.set(data.getlist('products'))
        elif data['requirements'] == 'services':
            lead.services.set(data.getlist('services'))
        else:
            lead.products.set(data.getlist('products'))
            lead.services.set(data.getlist('services'))

        messages.success(request, 'Lead added successfully!')
        return redirect('view_leads')

    # For GET request
    return render(request, 'add_lead.html', {
        'products': products,
        'services': services,
        'sales_persons': sales_persons,
        'follow_up_persons': follow_up_persons,
        'country_codes': [ ('+91', '🇮🇳 India'),
    ('+93', '🇦🇫 Afghanistan'),
    ('+355', '🇦🇱 Albania'),
    ('+213', '🇩🇿 Algeria'),
    ('+376', '🇦🇩 Andorra'),
    ('+244', '🇦🇴 Angola'),
    ('+1-268', '🇦🇬 Antigua and Barbuda'),
    ('+54', '🇦🇷 Argentina'),
    ('+374', '🇦🇲 Armenia'),
    ('+61', '🇦🇺 Australia'),
    ('+43', '🇦🇹 Austria'),
    ('+994', '🇦🇿 Azerbaijan'),
    ('+1-242', '🇧🇸 Bahamas'),
    ('+973', '🇧🇭 Bahrain'),
    ('+880', '🇧🇩 Bangladesh'),
    ('+1-246', '🇧🇧 Barbados'),
    ('+375', '🇧🇾 Belarus'),
    ('+32', '🇧🇪 Belgium'),
    ('+501', '🇧🇿 Belize'),
    ('+229', '🇧🇯 Benin'),
    ('+975', '🇧🇹 Bhutan'),
    ('+591', '🇧🇴 Bolivia'),
    ('+387', '🇧🇦 Bosnia and Herzegovina'),
    ('+267', '🇧🇼 Botswana'),
    ('+55', '🇧🇷 Brazil'),
    ('+673', '🇧🇳 Brunei'),
    ('+359', '🇧🇬 Bulgaria'),
    ('+226', '🇧🇫 Burkina Faso'),
    ('+257', '🇧🇮 Burundi'),
    ('+855', '🇰🇭 Cambodia'),
    ('+237', '🇨🇲 Cameroon'),
    ('+1', '🇨🇦 Canada'),
    ('+238', '🇨🇻 Cape Verde'),
    ('+236', '🇨🇫 Central African Republic'),
    ('+235', '🇹🇩 Chad'),
    ('+56', '🇨🇱 Chile'),
    ('+86', '🇨🇳 China'),
    ('+57', '🇨🇴 Colombia'),
    ('+269', '🇰🇲 Comoros'),
    ('+506', '🇨🇷 Costa Rica'),
    ('+385', '🇭🇷 Croatia'),
    ('+53', '🇨🇺 Cuba'),
    ('+357', '🇨🇾 Cyprus'),
    ('+420', '🇨🇿 Czech Republic'),
    ('+45', '🇩🇰 Denmark'),
    ('+253', '🇩🇯 Djibouti'),
    ('+1-767', '🇩🇲 Dominica'),
    ('+1-809', '🇩🇴 Dominican Republic'),
    ('+593', '🇪🇨 Ecuador'),
    ('+20', '🇪🇬 Egypt'),
    ('+503', '🇸🇻 El Salvador'),
    ('+240', '🇬🇶 Equatorial Guinea'),
    ('+291', '🇪🇷 Eritrea'),
    ('+372', '🇪🇪 Estonia'),
    ('+251', '🇪🇹 Ethiopia'),
    ('+679', '🇫🇯 Fiji'),
    ('+358', '🇫🇮 Finland'),
    ('+33', '🇫🇷 France'),
    ('+241', '🇬🇦 Gabon'),
    ('+220', '🇬🇲 Gambia'),
    ('+995', '🇬🇪 Georgia'),
    ('+49', '🇩🇪 Germany'),
    ('+233', '🇬🇭 Ghana'),
    ('+30', '🇬🇷 Greece'),
    ('+1-473', '🇬🇩 Grenada'),
    ('+502', '🇬🇹 Guatemala'),
    ('+224', '🇬🇳 Guinea'),
    ('+245', '🇬🇼 Guinea-Bissau'),
    ('+592', '🇬🇾 Guyana'),
    ('+509', '🇭🇹 Haiti'),
    ('+504', '🇭🇳 Honduras'),
    ('+36', '🇭🇺 Hungary'),
   
    ('+62', '🇮🇩 Indonesia'),
    ('+98', '🇮🇷 Iran'),
    ('+964', '🇮🇶 Iraq'),
    ('+353', '🇮🇪 Ireland'),
    ('+972', '🇮🇱 Israel'),
    ('+39', '🇮🇹 Italy'),
    ('+1-876', '🇯🇲 Jamaica'),
    ('+81', '🇯🇵 Japan'),
    ('+962', '🇯🇴 Jordan'),
    ('+7', '🇰🇿 Kazakhstan'),
    ('+254', '🇰🇪 Kenya'),
    ('+965', '🇰🇼 Kuwait'),
    ('+996', '🇰🇬 Kyrgyzstan'),
    ('+856', '🇱🇦 Laos'),
    ('+371', '🇱🇻 Latvia'),
    ('+961', '🇱🇧 Lebanon'),
    ('+266', '🇱🇸 Lesotho'),
    ('+231', '🇱🇷 Liberia'),
    ('+218', '🇱🇾 Libya'),
    ('+423', '🇱🇮 Liechtenstein'),
    ('+370', '🇱🇹 Lithuania'),
    ('+352', '🇱🇺 Luxembourg'),
    ('+261', '🇲🇬 Madagascar'),
    ('+265', '🇲🇼 Malawi'),
    ('+60', '🇲🇾 Malaysia'),
    ('+960', '🇲🇻 Maldives'),
    ('+223', '🇲🇱 Mali'),
    ('+356', '🇲🇹 Malta'),
    ('+222', '🇲🇷 Mauritania'),
    ('+230', '🇲🇺 Mauritius'),
    ('+52', '🇲🇽 Mexico'),
    ('+373', '🇲🇩 Moldova'),
    ('+377', '🇲🇨 Monaco'),
    ('+976', '🇲🇳 Mongolia'),
    ('+382', '🇲🇪 Montenegro'),
    ('+212', '🇲🇦 Morocco'),
    ('+258', '🇲🇿 Mozambique'),
    ('+95', '🇲🇲 Myanmar'),
    ('+264', '🇳🇦 Namibia'),
    ('+977', '🇳🇵 Nepal'),
    ('+31', '🇳🇱 Netherlands'),
    ('+64', '🇳🇿 New Zealand'),
    ('+505', '🇳🇮 Nicaragua'),
    ('+227', '🇳🇪 Niger'),
    ('+234', '🇳🇬 Nigeria'),
    ('+47', '🇳🇴 Norway'),
    ('+968', '🇴🇲 Oman'),
    ('+92', '🇵🇰 Pakistan'),
    ('+507', '🇵🇦 Panama'),
    ('+595', '🇵🇾 Paraguay'),
    ('+51', '🇵🇪 Peru'),
    ('+63', '🇵🇭 Philippines'),
    ('+48', '🇵🇱 Poland'),
    ('+351', '🇵🇹 Portugal'),
    ('+974', '🇶🇦 Qatar'),
    ('+40', '🇷🇴 Romania'),
    ('+7', '🇷🇺 Russia'),
    ('+250', '🇷🇼 Rwanda'),
    ('+966', '🇸🇦 Saudi Arabia'),
    ('+221', '🇸🇳 Senegal'),
    ('+381', '🇷🇸 Serbia'),
    ('+248', '🇸🇨 Seychelles'),
    ('+232', '🇸🇱 Sierra Leone'),
    ('+65', '🇸🇬 Singapore'),
    ('+421', '🇸🇰 Slovakia'),
    ('+386', '🇸🇮 Slovenia'),
    ('+27', '🇿🇦 South Africa'),
    ('+82', '🇰🇷 South Korea'),
    ('+34', '🇪🇸 Spain'),
    ('+94', '🇱🇰 Sri Lanka'),
    ('+249', '🇸🇩 Sudan'),
    ('+597', '🇸🇷 Suriname'),
    ('+46', '🇸🇪 Sweden'),
    ('+41', '🇨🇭 Switzerland'),
    ('+963', '🇸🇾 Syria'),
    ('+886', '🇹🇼 Taiwan'),
    ('+992', '🇹🇯 Tajikistan'),
    ('+255', '🇹🇿 Tanzania'),
    ('+66', '🇹🇭 Thailand'),
    ('+228', '🇹🇬 Togo'),
    ('+676', '🇹🇴 Tonga'),
    ('+216', '🇹🇳 Tunisia'),
    ('+90', '🇹🇷 Turkey'),
    ('+993', '🇹🇲 Turkmenistan'),
    ('+256', '🇺🇬 Uganda'),
    ('+380', '🇺🇦 Ukraine'),
    ('+971', '🇦🇪 United Arab Emirates'),
    ('+44', '🇬🇧 United Kingdom'),
    ('+1', '🇺🇸 United States'),
    ('+598', '🇺🇾 Uruguay'),
    ('+998', '🇺🇿 Uzbekistan'),
    ('+58', '🇻🇪 Venezuela'),
    ('+84', '🇻🇳 Vietnam'),
    ('+967', '🇾🇪 Yemen'),
    ('+260', '🇿🇲 Zambia'),
    ('+263', '🇿🇼 Zimbabwe')],
    })




from django.shortcuts import render, get_object_or_404
from .models import Lead
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import os
from .models import Lead

@login_required
def view_pdf(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    file_url = lead.file_upload.url if lead.file_upload else None
    file_ext = os.path.splitext(lead.file_upload.name)[1].lower() if lead.file_upload else ''

    is_pdf = file_ext == '.pdf'
    is_image = file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    is_word = file_ext in ['.doc', '.docx']

    return render(request, 'view_pdf.html', {
        'lead': lead,
        'file_url': file_url,
        'is_pdf': is_pdf,
        'is_image': is_image,
        'is_word': is_word
    })




from django.db.models import Q
from .models import Lead

@login_required
def view_leads(request):
    query = request.GET.get('q')
    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            Q(full_name__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'view_leads.html', {'leads': leads, 'query': query})




from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, time
from django.shortcuts import render
from .models import Lead

@login_required
def my_work(request):
    user = request.user
    today = now().date()
    leads = Lead.objects.filter(is_closed=False).distinct()
    lead_data = []

    for lead in leads:
        status = None
        followup_date = None
        assigned_to_user = False

        # 1st Follow-Up
        if not hasattr(lead, 'followup1'):
            if lead.follow_up_person == user:
                followup_date = lead.next_followup_date
                status = {'label': '1st Follow Up', 'url_name': 'follow_up_1'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup2'):
            f1 = lead.followup1
            if f1.next_followup_person == user:
                followup_date = f1.next_followup_date
                status = {'label': '2nd Follow Up', 'url_name': 'follow_up_2'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup3'):
            f2 = lead.followup2
            if f2.next_followup_person == user:
                followup_date = f2.next_followup_date
                status = {'label': '3rd Follow Up', 'url_name': 'follow_up_3'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup4'):
            f3 = lead.followup3
            if f3.next_followup_person == user:
                followup_date = f3.next_followup_date
                status = {'label': '4th Follow Up', 'url_name': 'follow_up_4'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup5'):
            f4 = lead.followup4
            if f4.next_followup_person == user:
                followup_date = f4.next_followup_date
                status = {'label': '5th Follow Up', 'url_name': 'follow_up_5'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup6'):
            f5 = lead.followup5
            if f5.next_followup_person == user:
                followup_date = f5.next_followup_date
                status = {'label': '6th Follow Up', 'url_name': 'follow_up_6'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup7'):
            f6 = lead.followup6
            if f6.next_followup_person == user:
                followup_date = f6.next_followup_date
                status = {'label': '7th Follow Up', 'url_name': 'follow_up_7'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup8'):
            f7 = lead.followup7
            if f7.next_followup_person == user:
                followup_date = f7.next_followup_date
                status = {'label': '8th Follow Up', 'url_name': 'follow_up_8'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup9'):
            f8 = lead.followup8
            if f8.next_followup_person == user:
                followup_date = f8.next_followup_date
                status = {'label': '9th Follow Up', 'url_name': 'follow_up_9'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup10'):
            f9 = lead.followup9
            if f9.next_followup_person == user:
                followup_date = f9.next_followup_date
                status = {'label': '10th Follow Up', 'url_name': 'follow_up_10'}
                assigned_to_user = True

        # ✅ Show if today's followup OR followup_date is None (N/A)
        if assigned_to_user and (followup_date == today or followup_date is None):
            lead_data.append({
                'lead': lead,
                'status': status,
                'followup_date': followup_date
            })

    lead_data.sort(
        key=lambda x: (
            datetime.combine(x['followup_date'], time.min)
            if isinstance(x['followup_date'], date) and not isinstance(x['followup_date'], datetime)
            else x['followup_date'] or datetime.max
        )
    )

    return render(request, 'my_work.html', {'lead_data': lead_data})



from django.shortcuts import render, get_object_or_404
from .models import Lead, FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10

def work_history(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    followups = []
    followup_models = [FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10]

    for model in followup_models:
        try:
            followup = model.objects.get(lead=lead)
        except model.DoesNotExist:
            followup = None
        followups.append(followup)

    return render(request, 'work_history.html', {
        'lead': lead,
        'followups': followups,
    })





from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from .models import Lead

@login_required
def pending_work(request):
    user = request.user
    today = now().date()
    leads = Lead.objects.filter(is_closed=False).distinct()
    lead_data = []

    for lead in leads:
        status = None
        followup_date = None
        assigned_to_user = False

        if not hasattr(lead, 'followup1'):
            if lead.follow_up_person == user:
                followup_date = lead.next_followup_date
                status = {'label': '1st Follow Up', 'url_name': 'follow_up_1'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup2'):
            f1 = lead.followup1
            if f1.next_followup_person == user:
                followup_date = f1.next_followup_date
                status = {'label': '2nd Follow Up', 'url_name': 'follow_up_2'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup3'):
            f2 = lead.followup2
            if f2.next_followup_person == user:
                followup_date = f2.next_followup_date
                status = {'label': '3rd Follow Up', 'url_name': 'follow_up_3'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup4'):
            f3 = lead.followup3
            if f3.next_followup_person == user:
                followup_date = f3.next_followup_date
                status = {'label': '4th Follow Up', 'url_name': 'follow_up_4'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup5'):
            f4 = lead.followup4
            if f4.next_followup_person == user:
                followup_date = f4.next_followup_date
                status = {'label': '5th Follow Up', 'url_name': 'follow_up_5'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup6'):
            f5 = lead.followup5
            if f5.next_followup_person == user:
                followup_date = f5.next_followup_date
                status = {'label': '6th Follow Up', 'url_name': 'follow_up_6'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup7'):
            f6 = lead.followup6
            if f6.next_followup_person == user:
                followup_date = f6.next_followup_date
                status = {'label': '7th Follow Up', 'url_name': 'follow_up_7'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup8'):
            f7 = lead.followup7
            if f7.next_followup_person == user:
                followup_date = f7.next_followup_date
                status = {'label': '8th Follow Up', 'url_name': 'follow_up_8'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup9'):
            f8 = lead.followup8
            if f8.next_followup_person == user:
                followup_date = f8.next_followup_date
                status = {'label': '9th Follow Up', 'url_name': 'follow_up_9'}
                assigned_to_user = True

        elif not hasattr(lead, 'followup10'):
            f9 = lead.followup9
            if f9.next_followup_person == user:
                followup_date = f9.next_followup_date
                status = {'label': '10th Follow Up', 'url_name': 'follow_up_10'}
                assigned_to_user = True

        # Show only overdue (follow-up date before today)
        if assigned_to_user and followup_date and followup_date < today:
            lead_data.append({
                'lead': lead,
                'status': status,
                'followup_date': followup_date
            })

    return render(request, 'pending_work.html', {'lead_data': lead_data})





@login_required
def completed_follow_up(request):
    # Leads that this user was previously responsible for but are now assigned to someone else
    past_leads = Lead.objects.filter(
        followup1__user=request.user
    ).exclude(followup1__next_followup_person=request.user)

    return render(request, 'completed_follow_up.html', {'lead_data': past_leads})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lead, CustomUser, FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lead, CustomUser, FollowUp1
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

@login_required
def follow_up_1(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if hasattr(lead, 'followup1'):
        return redirect('follow_up_2', lead_id=lead_id)

    if request.method == 'POST':
        customer_visited = request.POST.get('customer_visited') == 'yes'
        inspection_done = request.POST.get('inspection_done') == 'yes'
        quotation_given = request.POST.get('quotation_given') == 'yes'
        quotation_amount = request.POST.get('quotation_amount') or None
        description = request.POST.get('description')
        quotation_file = request.FILES.get('quotation_file')
        lead_type = request.POST.get('lead_type')
        close_lead = request.POST.get('close_lead') == 'on'  # Checkbox is "on" when selected
        win_status = request.POST.get('win_status')  # 'win' or 'loss'

        # Default values
        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead:
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'loss':
                close_status = 'Loss'
        else:
            close_status = 'Open'

            # Safely parse date
            next_followup_date_str = request.POST.get('next_followup_date')
            if next_followup_date_str:
                try:
                    next_followup_date = datetime.strptime(next_followup_date_str, '%Y-%m-%d').date()
                except ValueError:
                    next_followup_date = None

            # Get next follow-up person
            next_followup_person_id = request.POST.get('next_followup_person')
            if next_followup_person_id:
                try:
                    next_followup_person = CustomUser.objects.get(id=next_followup_person_id)
                except CustomUser.DoesNotExist:
                    next_followup_person = None

        # Create FollowUp1 record
        FollowUp1.objects.create(
            lead=lead,
            customer_visited=customer_visited,
            inspection_done=inspection_done,
            quotation_given=quotation_given,
            quotation_amount=quotation_amount,
            description=description,
            quotation_file=quotation_file,
            lead_type=lead_type,
            followup_person=request.user,
            next_followup_date=next_followup_date,
            next_followup_person=next_followup_person,
            close_status=close_status
        )

        # Update lead status
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.closed_by = request.user
            lead.save()
        else:
            if next_followup_person:
                lead.follow_up_person = next_followup_person
                lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_1.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, FollowUp2, CustomUser
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, FollowUp2, CustomUser

@login_required
def follow_up_2(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get followup fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp3 entry
        FollowUp2.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.closed_by = request.user  # <-- add this line

            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_2.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_3(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get followup fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp3 entry
        FollowUp3.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_3.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lead, FollowUp4, CustomUser  # Make sure FollowUp4 model exists

@login_required
def follow_up_4(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp4.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_4.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_5(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp5.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_5.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })





@login_required
def follow_up_6(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp6.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_6.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


@login_required
def follow_up_7(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp7.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_7.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


@login_required
def follow_up_8(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp8.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_8.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_9(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp9.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_9.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_10(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open
            close_status = 'Open'

        # Create FollowUp10 entry (no next follow-up fields)
        FollowUp10.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_10.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })

from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Lead

from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Lead

@require_POST
def close_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    # Set is_closed to True
    lead.is_closed = True

    # Determine win or lose
    status = request.POST.get('win_status')
    if status == 'win':
        lead.win_status = True
    else:
        lead.win_status = False

    lead.save()
    return redirect('my_work')  # or wherever you want to go


@login_required
def assign_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == 'POST':
        new_user_id = request.POST.get('new_assignee')
        if new_user_id:
            new_user = get_object_or_404(CustomUser, id=new_user_id)
            lead.follow_up_person = new_user
            lead.save()
            messages.success(request, f"Lead reassigned to {new_user.username}.")
    
    return redirect('my_work')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead, CustomUser
from django.contrib import messages

# @login_required
# def closed_leads(request):
#     closed = Lead.objects.filter(is_closed=True, follow_up_person=request.user)
#     operation_users = CustomUser.objects.filter(role='Operations')
#     return render(request, 'close_lead.html', {
#         'closed_leads': closed,
#         'operation_users': operation_users
#     })


@login_required
def closed_leads(request):
    # Leads closed via follow-up (as you're already displaying)
    closed_followup = Lead.objects.filter(is_closed=True, follow_up_person=request.user)

    # Leads closed directly (without follow-up)
    direct_closed = Lead.objects.filter(is_closed=True, follow_up_person__isnull=True)

    operation_users = CustomUser.objects.filter(role='Operations')

    return render(request, 'close_lead.html', {
        'closed_leads': closed_followup,
        'direct_closed_leads': direct_closed,
        'operation_users': operation_users
    })





# start

# def quotation(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')
#         lead = Lead.objects.filter(mobile_number=mobile).first()

#         quotation = Quotation()

#         if lead:
#             quotation.lead = lead
#             quotation.full_name = lead.full_name
#             quotation.mobile = lead.mobile_number
#             quotation.email = lead.email
#             quotation.address = lead.address
#             quotation.save()  # Save first so we can add M2M later
#             quotation.products.set(lead.products.all())
#             quotation.services.set(lead.services.all())

#         # Add logic to save quantity, gst, and other fields if they are part of form
#         quotation.quantity = request.POST.get('quantity')
#         quotation.gst_percentage = request.POST.get('gst_percentage')

#         quotation.save()

#         messages.success(request, 'Quotation created successfully.')
#         return redirect('my_work')  # Adjust according to your flow

#     return render(request, 'quotation.html')





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lead, Quotation, Product, Service
from .models import QuotationProduct, QuotationService



# def quotation(request):
#     context = {
#         'products': Product.objects.all(),
#         'services': Service.objects.all()
#     }

#     if request.method == 'POST':
#         if 'fetch_lead' in request.POST:
#             mobile = request.POST.get('mobile')
#             lead = Lead.objects.filter(mobile_number=mobile).first()
#             if lead:
#                 context['lead'] = lead
#             else:
#                 messages.error(request, 'No lead found with this mobile number.')

#         elif 'submit_quotation' in request.POST:
#             mobile = request.POST.get('mobile')
#             lead = Lead.objects.filter(mobile_number=mobile).first()

#             if lead:
#                 quotation = Quotation.objects.create(
#                     lead=lead,
#                     full_name=request.POST.get('full_name') or lead.full_name,
#                     mobile=lead.mobile_number,
#                     email=request.POST.get('email') or lead.email,
#                     address=request.POST.get('address') or lead.address,

                    
#                     # actual_price=request.POST.get('actual_price') or None,
#                     # quantity=request.POST.get('quantity') or None,
#                     # gst_percentage=request.POST.get('gst_percentage') or None,
#                     cgst=request.POST.get('cgst') or None,
#                     sgst=request.POST.get('sgst') or None,
#                     igst=request.POST.get('igst') or None,
#                     gst_total=request.POST.get('gst_total') or None,
#                     total_amount=request.POST.get('total_amount') or None,
#                     total_amount_with_gst=request.POST.get('total_amount_with_gst') or None,
#                 )

#                 selected_products = request.POST.getlist('products')
#                 for pid in selected_products:
#                     price = request.POST.get(f'product_price_{pid}') or 0
#                     quantity = request.POST.get(f'product_quantity_{pid}') or 1
#                     gst_percent = request.POST.get(f'product_gst_{pid}') or 0

#                     QuotationProduct.objects.create(
#                         quotation=quotation,
#                         product_id=pid,
#                         actual_price=price,
#                         quantity=quantity,
#                         gst_percent=gst_percent
#                         )

#                 selected_services = request.POST.getlist('services')
#                 for sid in selected_services:
#                     price = request.POST.get(f'service_price_{sid}') or 0
#                     quantity = request.POST.get(f'service_quantity_{sid}') or 1
#                     gst_percent = request.POST.get(f'service_gst_{sid}') or 0

#                     QuotationService.objects.create(
#                         quotation=quotation,
#                         service_id=sid,
#                         actual_price=price,
#                         quantity=quantity,
#                         gst_percent=gst_percent
#                         )        


#                 messages.success(request, 'Quotation created successfully.')
#                 return redirect('my_work')
#             else:
#                 messages.error(request, 'No lead found to create quotation.')

#     return render(request, 'quotation.html', context)




def quotation(request):
    context = {
        'products': Product.objects.all(),
        'services': Service.objects.all()
    }

    if request.method == 'POST':
        if 'fetch_lead' in request.POST:
            mobile = request.POST.get('mobile')
            lead = Lead.objects.filter(mobile_number=mobile).first()
            if lead:
                context['lead'] = lead
            else:
                messages.error(request, 'No lead found with this mobile number.')

        elif 'submit_quotation' in request.POST:
            mobile = request.POST.get('mobile')
            lead = Lead.objects.filter(mobile_number=mobile).first()
            enable_gst = 'enable_gst' in request.POST  # Check if GST is enabled

            if lead:
                quotation = Quotation.objects.create(
                    lead=lead,
                    full_name=request.POST.get('full_name') or lead.full_name,
                    mobile=lead.mobile_number,
                    email=request.POST.get('email') or lead.email,
                    address=request.POST.get('address') or lead.address,
                    enable_gst=enable_gst,
                    cgst=request.POST.get('cgst') if enable_gst else None,
                    sgst=request.POST.get('sgst') if enable_gst else None,
                    igst=request.POST.get('igst') if enable_gst else None,
                    gst_total=request.POST.get('gst_total') if enable_gst else None,
                    total_amount=request.POST.get('total_amount') if enable_gst else request.POST.get('simple_total'),
                    total_amount_with_gst=request.POST.get('total_amount_with_gst') if enable_gst else request.POST.get('simple_total'),
                )

                selected_products = request.POST.getlist('products')
                for pid in selected_products:
                    price = request.POST.get(f'product_price_{pid}') or 0
                    quantity = request.POST.get(f'product_quantity_{pid}') or 1
                    gst_percent = request.POST.get(f'product_gst_{pid}') or 0 if enable_gst else 0

                    QuotationProduct.objects.create(
                        quotation=quotation,
                        product_id=pid,
                        actual_price=price,
                        quantity=quantity,
                        gst_percent=gst_percent
                    )

                selected_services = request.POST.getlist('services')
                for sid in selected_services:
                    price = request.POST.get(f'service_price_{sid}') or 0
                    quantity = request.POST.get(f'service_quantity_{sid}') or 1
                    gst_percent = request.POST.get(f'service_gst_{sid}') or 0 if enable_gst else 0

                    QuotationService.objects.create(
                        quotation=quotation,
                        service_id=sid,
                        actual_price=price,
                        quantity=quantity,
                        gst_percent=gst_percent
                    )        

                messages.success(request, 'Quotation created successfully.')
                return redirect('my_work')
            else:
                messages.error(request, 'No lead found to create quotation.')

    return render(request, 'quotation.html', context)





from django.shortcuts import get_object_or_404

def quotation_detail(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Calculate product details
    quotation_products = []
    for qp in QuotationProduct.objects.filter(quotation=quotation):
        subtotal = qp.actual_price * qp.quantity
        gst_amount = subtotal * qp.gst_percent / 100
        total = subtotal + gst_amount
        quotation_products.append({
            'product': qp.product,
            'actual_price': qp.actual_price,
            'quantity': qp.quantity,
            'gst_percent': qp.gst_percent,
            'subtotal': subtotal,
            'gst_amount': gst_amount,
            'total': total
        })
    
    # Calculate service details
    quotation_services = []
    for qs in QuotationService.objects.filter(quotation=quotation):
        subtotal = qs.actual_price * qs.quantity
        gst_amount = subtotal * qs.gst_percent / 100
        total = subtotal + gst_amount
        quotation_services.append({
            'service': qs.service,
            'actual_price': qs.actual_price,
            'quantity': qs.quantity,
            'gst_percent': qs.gst_percent,
            'subtotal': subtotal,
            'gst_amount': gst_amount,
            'total': total
        })
    
    context = {
        'quotation': quotation,
        'quotation_products': quotation_products,
        'quotation_services': quotation_services
    }
    
    return render(request, 'quotation_detail.html', context)



def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-id')  # latest first
    return render(request, 'quotation_list.html', {'quotations': quotations})



@login_required
def assign_to_operations(request, lead_id):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=lead_id)
        operation_user_id = request.POST.get('operation_user_id')
        try:
            operation_user = CustomUser.objects.get(id=operation_user_id, role='Operations')
            lead.assigned_to_operations = operation_user
            lead.save()
            messages.success(request, "Lead assigned successfully to Operations.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid operations user selected.")
    return redirect('closed_leads')


from django.shortcuts import render, get_object_or_404
from .models import Lead
from django.contrib.auth.decorators import login_required

@login_required
def operation_lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id, assigned_to_operations=request.user)
    return render(request, 'operation_lead_detail.html', {'lead': lead})



@login_required
def operations_assigned_leads(request):
    leads = Lead.objects.filter(assigned_to_operations=request.user)
    print("Logged in user ID:", request.user.id)
    print("Assigned leads count:", leads.count())
    for lead in leads:
        print(lead.full_name, "->", lead.assigned_to_operations_id)
    return render(request, 'operations_assigned_leads.html', {'assigned_leads': leads})

