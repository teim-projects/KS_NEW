from . import views
from django.urls import path # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', views.index, name='index'),
   path('signup/', views.signup, name='signup'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard'),
   path('operations_dashboard/', views.operations_dashboard, name='operations_dashboard'),
   path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
   path('finance_dashboard/', views.finance_dashboard, name='finance_dashboard'),
   path('create_user/', views.create_user, name='create_user'),
   path('requirements/', views.requirements_dashboard, name='requirements_dashboard'),
   path('lead/pdf/<int:lead_id>/', views.view_pdf, name='view_pdf'),



    # Quotation Term URLs
    path('quotation-terms/', views.quotation_term_list, name='quotation_term_list'),
    path('quotation-terms/add/', views.add_quotation_term, name='add_quotation_term'),
    path('quotation-terms/edit/<int:pk>/', views.edit_quotation_term, name='edit_quotation_term'),
    path('quotation-terms/delete/<int:pk>/', views.delete_quotation_term, name='delete_quotation_term'),

    # Invoice Term URLs
    path('invoice-terms/', views.invoice_term_list, name='invoice_term_list'),
    path('invoice-terms/add/', views.add_invoice_term, name='add_invoice_term'),
    path('invoice-terms/edit/<int:pk>/', views.edit_invoice_term, name='edit_invoice_term'),
    path('invoice-terms/delete/<int:pk>/', views.delete_invoice_term, name='delete_invoice_term'),

    path('users/', views.view_users, name='view_users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    path('operations/leads/', views.operations_assigned_leads, name='operations_assigned_leads'),
    path('assign-to-operations/<int:lead_id>/', views.assign_to_operations, name='assign_to_operations'),
    path('operations/lead/<int:lead_id>/', views.operation_lead_detail, name='operation_lead_detail'),



 
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('service/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('service/edit/<int:pk>/', views.edit_service, name='edit_service'),
   path('add_lead/', views.add_lead, name='add_lead'),
    path('view-leads/', views.view_leads, name='view_leads'),
   #  path('edit-lead/<int:pk>/', views.edit_lead, name='edit_lead'),
    path('my-work/', views.my_work, name='my_work'),
    path('pending-work/', views.pending_work, name='pending_work'),

    path('completed-follow-up/', views.completed_follow_up, name='completed_follow_up'),

    path('followup1/<int:lead_id>/', views.follow_up_1, name='follow_up_1'),
    path('followup2/<int:lead_id>/', views.follow_up_2, name='follow_up_2'),
    path('followup3/<int:lead_id>/', views.follow_up_3, name='follow_up_3'),
    path('followup4/<int:lead_id>/', views.follow_up_4, name='follow_up_4'),
    path('followup5/<int:lead_id>/', views.follow_up_5, name='follow_up_5'),
    path('followup6/<int:lead_id>/', views.follow_up_6, name='follow_up_6'),
    path('followup7/<int:lead_id>/', views.follow_up_7, name='follow_up_7'),
    path('followup8/<int:lead_id>/', views.follow_up_8, name='follow_up_8'),
    path('followup9/<int:lead_id>/', views.follow_up_9, name='follow_up_9'),
    path('followup10/<int:lead_id>/', views.follow_up_10, name='follow_up_10'),
    path('close-lead/<int:lead_id>/', views.close_lead, name='close_lead'),
    path('assign-lead/<int:lead_id>/', views.assign_lead, name='assign_lead'),
    path('closed-leads/', views.closed_leads, name='closed_leads'),
    path('work_history/<int:lead_id>/', views.work_history, name='work_history'),
    # start

    path('quotation/',views.quotation,name='quotation'),
    # path('quotation_detail/', views.quotation_detail, name='quotation_detail'),
    
    path('quotation_detail/<int:quotation_id>/', views.quotation_detail, name='quotation_detail'),



    path('quotations/', views.quotation_list, name='quotation_list'),   
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)