import json
from urllib.parse import parse_qs
from urllib.parse import urlparse

import requests
from rest_framework.response import Response
from rest_framework.views import APIView

url = "https://secure.3gdirectpay.com/API/v7/index.php"
company_token = "EB310B77-FE73-427B-B3BB-97F19A0D70EA"
payment_amount = 1

# Credit Card Details here.
card_number = '5247490000208913'
card_expiry_date = '0323'
card_cvv = '163'
card_holder_name = 'Jackson Tembo'


def get_transaction_token(payment_url):
    """
    get transaction token from given payment url
    :param payment_url:
    :return:
    """
    if payment_url is not None:
        parsed_url = urlparse(payment_url)
        transaction_token = parse_qs(parsed_url.query)['ID'][0]
        return transaction_token


class ReduceAmount(APIView):
    def post(self, request):
        """
        Reduce the data package amount to 1 kwacha.
        :param request:
        :return:
        """
        payment_url = request.data.get('payment_url', None)
        if payment_url is not None:
            transaction_token = get_transaction_token(payment_url)
            data = {"Request": "UpdateToken", "CompanyToken": company_token, "TransactionToken": transaction_token,
                    "PaymentAmount": payment_amount}

            r = requests.post(url, data=json.dumps(data))
            if r.json().get('Code', 1) == '000':
                return Response({'status': 'success', 'message': 'amount has been reduced successfully'})
            else:
                return Response({'status': 'failed', 'message': 'this payment url cannot be updated.'})


class PayInvoice(APIView):
    def post(self, request):
        """
        Make payment for the invoice of the given url.
        :param request:
        :return:
        """
        payment_url = request.data.get('payment_url', None)
        if payment_url is not None:
            data = {
                "Request": "chargeTokenCreditCard", "CompanyToken": company_token,
                "TransactionToken": get_transaction_token(payment_url),
                "CreditCardNumber": card_number, "CreditCardExpiry": card_expiry_date,
                "CreditCardCVV": card_cvv, "CardHolderName": card_holder_name,
            }
            r = requests.post(url, data=json.dumps(data))
            if r.json().get('Code', 1) == '000':
                return Response({'status': 'success', 'message': 'Payment successful'})
            else:
                return Response(r.json())

