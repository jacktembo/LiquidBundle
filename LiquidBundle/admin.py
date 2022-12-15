from django.contrib import admin
from .models import *


@admin.register(LiquidDataPackage)
class LiquidDataPackageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price', 'description', 'validity'
    ]


@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'website', 'dpo_company_token', 'active_status',
    ]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'phone_number', 'balance'
    ]


@admin.register(SavedTransaction)
class SavedTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'date_time_created', 'amount',
        'reference_number', 'request_reference', 'product_id', 'session_uuid',
        'phone_number', 'type'
    ]


@admin.register(CompletedTransaction)
class CompletedTransactionAdmin(admin.ModelAdmin):
    list_display = ['date_time_created', 'type', 'package', 'lte_number', 'user']

