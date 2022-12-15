import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .api_views import get_transaction_token
import requests
from . import headless_selenium

url = "https://secure.3gdirectpay.com/API/v7/index.php"


def index(request):
    return HttpResponse('Welcome! Thank you for using our service')


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
        data = {"Request": "UpdateToken", "CompanyToken": company_token, "TransactionToken": transaction_token,
                "PaymentAmount": payment_amount}

        r = requests.post(url, data=json.dumps(data))
        if r.json().get('Code', 1) == '000':
            CompletedTransaction.objects.create(
                type='Sale', lte_number='N/A', user=request.user
            )
            context = {
                'transaction_token': transaction_token,
            }
            return render(request, 'success_amount_reduced.html', context)
        else:
            return HttpResponse('Something went wrong. Please try again')


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
