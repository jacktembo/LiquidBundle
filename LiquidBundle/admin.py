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


@admin.register(SavedTransaction)
class SavedTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'date_time_created', 'amount',
        'reference_number', 'request_reference', 'product_id', 'session_uuid',
        'phone_number', 'type'
    ]


@admin.register(CompletedTransaction)
class CompletedTransactionAdmin(admin.ModelAdmin):
    list_display = ['date_time_created', 'type', 'package', 'lte_number', 'user', 'amount', 'description']
    list_filter = [
        'date_time_created', 'user'
    ]


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'available_balance', 'minimum_deposit',
    ]


@admin.register(KazangSession)
class KazangSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_uuid', 'date_time_created'
    ]
    list_filter = ['date_time_created']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number', 'amount', 'reference_number', 'session_uuid'
    ]
    list_filter = ['session_uuid']
