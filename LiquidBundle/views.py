import json

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import headless_selenium
from . import kazang
from .api_views import get_transaction_token
from .models import *

url = "https://secure.3gdirectpay.com/API/v7/index.php"


def index(request):
    return HttpResponse('Welcome! Thank you for using our service')


@login_required(login_url='/login/')
def reduce_amount(request):
    if request.method == 'GET':
        service_companies = ServiceCompany.objects.all()
        context = {
            'service_companies': service_companies
        }
        return render(request, 'reduce_amount.html', context)
    else:
        service_company = ServiceCompany.objects.get(id=int(request.POST.get('service-company', None)))
        company_token = service_company.dpo_company_token
        payment_url = request.POST.get('payment-url', None)
        transaction_token = get_transaction_token(payment_url)
        payment_amount = 1
        data = {
            "Request": "updateToken", "CompanyToken": company_token,
            "TransactionToken": transaction_token, "CustomerEmail": "lusakazambia@proton.me",
            "CustomerFirstName": "John", "CustomerLastName": "Smith", "CustomerAddress": "Lusaka 10101",
            "CustomerPhone": "0977777777", "PaymentAmount": payment_amount
        }
        data2 = {
            "Request": "verifyToken", "CompanyToken": company_token,
            "TransactionToken": transaction_token,
        }
        verify_transaction = requests.post(url, json=data2)
        transaction_amount = verify_transaction.json().get('TransactionAmount', None)
        r = requests.post(url, data=json.dumps(data))
        if r.json().get('Code', 1) == '000':
            CompletedTransaction.objects.create(
                type='Sale', lte_number='N/A', user=request.user, amount=float(transaction_amount),
                description=verify_transaction.json().get('ServiceDescription', None)
            )
            context = {
                'transaction_token': transaction_token,
            }
            return render(request, 'success_amount_reduced.html', context)
        else:
            return HttpResponse('Something went wrong. Please try again')


@login_required(login_url='/login/')
def buy_liquid_bundle(request):
    packages = LiquidDataPackage.objects.all()
    if request.method == 'GET':
        context = {
            'packages': packages,
        }
        return render(request, 'buy_liquid_bundle.html', context)
    else:
        package = request.POST.get('package', None)
        package = LiquidDataPackage.objects.get(identifier=int(package))
        headless_selenium.package = package.identifier
        lte_number = request.POST.get('lte-number', None)
        payment_url = headless_selenium.automate(lte_number, package)
        return redirect(payment_url)


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('reduce-amount')
        return render(request, 'login.html')
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('reduce-amount')
    return redirect('login')


def logout_view(request):
    return logout(request)


session_uuid = kazang.session_uuid


@login_required(login_url='/login/')
def mobile_payment(request):
    if request.method == 'GET':
        return render(request, 'mobile_payment.html')
    deposit_amount = float(request.POST.get('amount', None)) * 100
    phone_number = request.POST.get('phone-number', None)
    pay = kazang.airtel_pay_payment(phone_number, deposit_amount)
    if pay.get('response_code', None) == '0':
        PaymentTransaction.objects.create(
            session_uuid=session_uuid, phone_number=phone_number,
            amount=deposit_amount, reference_number=pay.get('airtel_reference', None),
        )
        context = {
            'reference': pay.get('airtel_reference', None),
            'phone': phone_number, 'amount': deposit_amount
        }
        return render(request, 'pay_query.html', context)


@login_required(login_url='/login/')
def pay_query(request):
    if request.method == 'GET':
        return render(request, 'pay_query.html')

    reference_number = request.POST.get('reference', None)
    phone_number = request.POST.get('phone')
    amount = request.POST.get('amount', None)
    user_wallet = request.user.userwallet
    query = kazang.airtel_pay_query(phone_number, amount, reference_number)
    if query.get('response_code', None) == '0':
        user_wallet.available_balance += float(amount) / 100
        user_wallet.save()
        kazang.airtel_cash_in('0971977252', float(amount))
        return render(request, 'payment_successful.html')
    return HttpResponse(query.get('response_message', None))
