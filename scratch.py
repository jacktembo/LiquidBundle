import requests

url = "https://secure.3gdirectpay.com/API/v7/index.php"
data = {'Request': 'updateToken', 'CompanyToken': 'DAFCFA0F-E11D-40D6-A65B-6D42EDD6AC65',
        'TransactionToken': '4C300B03-680D-4136-BAD0-DA26527930F1'}
r = requests.post(url, json=data)
print(r.text)